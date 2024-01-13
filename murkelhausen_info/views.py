import logging
from datetime import datetime, timedelta
from typing import Callable

from cachetools import TTLCache, cached
from django.db.models import Avg, IntegerField
from django.db.models.functions import Cast, Extract, TruncHour
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic.edit import FormMixin

from murkelhausen_info import gymbroich, mheg, ruhrbahn, weather
from murkelhausen_info.forms import StationForm
from murkelhausen_info.models import PowerData
from murkelhausen_info.tables import (
    DeparturesTable,
    MuellTable,
    TemperatureTable,
    VertretungsplanTable,
    WeatherTable,
)

logger = logging.getLogger(__name__)


class IndexView(View):
    template_name = "murkelhausen_info/index.html"

    def get(self, request, *args, **kwargs):
        muell_termine = mheg.get_muelltermine_for_this_week()
        owm_data = weather.get_weather_data_muelheim()

        context = {
            "weather_data": owm_data,
            "muell_termine": muell_termine,
        }
        return render(request, self.template_name, context)


class PowerView(View):
    @staticmethod
    @cached(cache=TTLCache(maxsize=10, ttl=60 * 5))  # 5 minutes
    def _get_power_data_complete(
        sensor_name: str, time_aggregate_callable: Callable
    ) -> list[dict]:
        power_data = (
            PowerData.objects.filter(sensorname__icontains=sensor_name)
            .annotate(tstamp_truncated=time_aggregate_callable("tstamp"))
            .values("tstamp_truncated")
            .annotate(power_current=Cast(Avg("power_current"), IntegerField()))
            .annotate(power_total=Cast(Avg("power_total"), IntegerField()))
            .annotate(tstamp_epoch=Extract("tstamp_truncated", "epoch") * 1000)
            .values("tstamp_epoch", "power_current", "power_total")
        )
        logger.info(f"Retrieved {len(power_data)} aggregated power data from database.")
        return list(power_data)

    @staticmethod
    @cached(cache=TTLCache(maxsize=10, ttl=60 * 5))  # 5 minutes
    def _get_power_data_all_last_week(sensor_name: str) -> list[dict]:
        power_data = (
            PowerData.objects.filter(sensorname__icontains=sensor_name)
            .values("tstamp", "sensorname", "power_current", "power_total")
            .filter(tstamp__gte=(datetime.now() - timedelta(days=7)).date().isoformat())
            .annotate(tstamp_epoch=Extract("tstamp", "epoch") * 1000)
            .order_by("tstamp_epoch")
            .values("tstamp_epoch", "sensorname", "power_current", "power_total")
        )
        logger.info(
            f"Retrieved {len(power_data)} fine grained power data for last week from database."
        )
        return list(power_data)

    def get(self, request, *args, **kwargs):
        logger.info("Getting haushalt power data complete.")
        power_data_haushalt_complete = self._get_power_data_complete(
            "stromhaushalt", TruncHour
        )
        logger.info("Getting haushalt power data last week minutely.")
        power_data_haushalt_last_week = self._get_power_data_all_last_week(
            "stromhaushalt"
        )
        logger.info("Getting waermepumpe power data complete.")
        power_data_waermepumpe_complete = self._get_power_data_complete(
            "stromwaermepumpe", TruncHour
        )
        logger.info("Getting waermepumpe power data last week minutely.")
        power_data_waermepumpe_last_week = self._get_power_data_all_last_week(
            "stromwaermepumpe"
        )
        logger.info("Rendering power template.")
        return render(
            request,
            "murkelhausen_info/power.html",
            context={
                "power_data_haushalt_complete": power_data_haushalt_complete,
                "power_data_haushalt_last_week": power_data_haushalt_last_week,
                "power_data_waermepumpe_complete": power_data_waermepumpe_complete,
                "power_data_waermepumpe_last_week": power_data_waermepumpe_last_week,
            },
        )


class DepartureView(View, FormMixin):
    template_name = "murkelhausen_info/departures.html"

    @staticmethod
    def _get_data(station: str) -> list[dict]:
        station_id = ruhrbahn.get_stations().get_station_id(station, "Mülheim")
        logger.info(f"Retrieved station id {station_id} for station {station}.")

        departure_data = ruhrbahn.get_departure_data(station_id)
        departures = departure_data.get_departure_list()
        data = [
            {
                "richtung": departure.richtung,
                "departure_time": departure.planned_departure_time,
                "delay": departure.delay,
                "linie": departure.servingLine.number,
                "platform": departure.platform,
            }
            for departure in departures
        ]
        logger.info(f"Retrieved {len(data)} departures for station {station}.")

        return data

    def get(self, request, *args, **kwargs):
        station = self.request.session.get("station")
        if station is None:
            station = ruhrbahn.STATIONS[0]
            logger.info(
                f"Setting station to default ({station}) as station is empty in session cache."
            )
        form = StationForm()
        form.initial["station"] = ruhrbahn.STATIONS.index(station)
        departure_data = self._get_data(station)
        table = DeparturesTable(departure_data[:20])
        table.paginate(page=request.GET.get("page", 1), per_page=20)
        logger.info(f"Rendering departures template for {station=}.")
        return render(request, self.template_name, {"form": form, "table": table})

    def post(self, request, *args, **kwargs):
        form = StationForm(request.POST)
        if form.is_valid():
            station_position = form.cleaned_data["station"]
            station = ruhrbahn.STATIONS[int(station_position)]
            logger.info(f"Setting station to {station} in session cache.")
            self.request.session["station"] = station

        return HttpResponseRedirect(request.path_info)


class WeatherView(View):
    @staticmethod
    def _get_weather_table_data(owm_data: weather.OWMOneCall, request) -> list[dict]:
        today = owm_data.daily[0]
        tomorrow = owm_data.daily[1]
        data = {
            "Temperatur": {
                "current": owm_data.current.temp_unit,
                "forecast_today": TemperatureTable(
                    [
                        {"zeitpunkt": "Morgens", "wert": today.temp.morn_unit},
                        {"zeitpunkt": "Tags", "wert": today.temp.day_unit},
                        {"zeitpunkt": "Abends", "wert": today.temp.eve_unit},
                        {"zeitpunkt": "Nachts", "wert": today.temp.night_unit},
                    ]
                ).as_html(request),
                "forecast_tomorrow": TemperatureTable(
                    [
                        {"zeitpunkt": "Morgens", "wert": tomorrow.temp.morn_unit},
                        {"zeitpunkt": "Tags", "wert": tomorrow.temp.day_unit},
                        {"zeitpunkt": "Abends", "wert": tomorrow.temp.eve_unit},
                        {"zeitpunkt": "Nachts", "wert": tomorrow.temp.night_unit},
                    ]
                ).as_html(request),
            },
            "Gefühlt": {
                "current": owm_data.current.feels_like_unit,
                "forecast_today": TemperatureTable(
                    [
                        {"zeitpunkt": "Morgens", "wert": today.feels_like.morn_unit},
                        {"zeitpunkt": "Tags", "wert": today.feels_like.day_unit},
                        {"zeitpunkt": "Abends", "wert": today.feels_like.eve_unit},
                        {"zeitpunkt": "Nachts", "wert": today.feels_like.night_unit},
                    ]
                ).as_html(request),
                "forecast_tomorrow": TemperatureTable(
                    [
                        {
                            "zeitpunkt": "Morgens",
                            "wert": tomorrow.feels_like.morn_unit,
                        },
                        {"zeitpunkt": "Tags", "wert": tomorrow.feels_like.day_unit},
                        {"zeitpunkt": "Abends", "wert": tomorrow.feels_like.eve_unit},
                        {"zeitpunkt": "Nachts", "wert": tomorrow.feels_like.night_unit},
                    ]
                ).as_html(request),
            },
            "Regen": {
                "current": owm_data.current.rain_unit,
                "forecast_today": today.rain_unit,
                "forecast_tomorrow": tomorrow.rain_unit,
            },
            "Regenwahrscheinlichkeit": {
                "current": owm_data.current_pop_unit,
                "forecast_today": today.pop_unit,
                "forecast_tomorrow": tomorrow.pop_unit,
            },
            "Schnee": {
                "current": owm_data.current.snow_unit,
                "forecast_today": today.snow_unit,
                "forecast_tomorrow": tomorrow.snow_unit,
            },
            "Luftfeuchtigkeit": {
                "current": owm_data.current.humidity_unit,
                "forecast_today": today.humidity_unit,
                "forecast_tomorrow": tomorrow.humidity_unit,
            },
            "Bewölkung": {
                "current": owm_data.current.clouds_unit,
                "forecast_today": today.clouds_unit,
                "forecast_tomorrow": tomorrow.clouds_unit,
            },
            "Windgeschwindigkeit": {
                "current": owm_data.current.wind_speed_unit,
                "forecast_today": today.wind_speed_unit,
                "forecast_tomorrow": tomorrow.wind_speed_unit,
            },
            "Windrichtung": {
                "current": owm_data.current.wind_direction,
                "forecast_today": today.wind_direction,
                "forecast_tomorrow": tomorrow.wind_direction,
            },
            "Sichtweite": {
                "current": owm_data.current.visibility_unit,
                "forecast_today": " ",
                "forecast_tomorrow": " ",
                "comment": "max. 10 km",
            },
            "UV Index": {
                "current": owm_data.current.uvi_unit,
                "forecast_today": " ",
                "forecast_tomorrow": " ",
                "comment": mark_safe(
                    "<a href='https://de.wikipedia.org/wiki/UV-Index' target='_blank'>0 - 11+</a>"
                ),
            },
            "Taupunkt": {
                "current": owm_data.current.dew_point_unit,
                "forecast_today": today.dew_point_unit,
                "forecast_tomorrow": tomorrow.dew_point_unit,
                "comment": mark_safe(
                    "<a href='https://https://de.wikipedia.org/wiki/Taupunkt' target='_blank'>Wikipedia</a>"
                ),
            },
            "Luftdruck": {
                "current": owm_data.current.pressure_unit,
                "forecast_today": today.pressure_unit,
                "forecast_tomorrow": tomorrow.pressure_unit,
            },
        }
        if not (owm_data.current.snow_unit or today.snow_unit or tomorrow.snow_unit):
            del data["Schnee"]

        transformed_data = []
        for attribute, values in data.items():
            transformed_data.append(
                {
                    "attribute": attribute,
                    "current": values.get("current", None),
                    "forecast_today": values.get("forecast_today", None),
                    "forecast_tomorrow": values.get("forecast_tomorrow", None),
                    "comment": values.get("comment", ""),
                }
            )
        return transformed_data

    def get(self, request, *args, **kwargs):
        owm_data = weather.get_weather_data_muelheim()
        weather_table = WeatherTable(self._get_weather_table_data(owm_data, request))

        return render(
            request,
            "murkelhausen_info/weather.html",
            context={
                "weather_data": owm_data,
                "weather_table": weather_table,
            },
        )


class MuellView(View):
    template_name = "murkelhausen_info/muell.html"

    def get(self, request, *args, **kwargs):
        termine = mheg.get_muelltermine_for_home()
        logger.info(f"Retrieved {len(termine)} Mülltermine from unofficial API.")
        data = [
            {
                "day": termin.day,
                "art": termin.art,
                "delta_days": termin.delta_days,
            }
            for termin in termine
        ]
        table = MuellTable(data)
        table.paginate(page=request.GET.get("page", 1), per_page=20)
        return render(request, self.template_name, {"table": table})


class VertretungsplanView(View):
    template_name = "murkelhausen_info/vertretungsplan.html"

    def get(self, request, *args, **kwargs):
        dates = gymbroich.get_vertretungsplan_dates()

        vertretungsplaene = []
        for date in dates:
            logger.info(f"Generating vertretungsplan table for {date=}.")
            plan = gymbroich.get_vertretungsplan(date)

            plaene_transformed = [
                {
                    "classes": ", ".join(event.classes),
                    "lessons": ", ".join(str(ele) for ele in event.lessons),
                    "previousSubject": event.previousSubject,
                    "subject": event.subject,
                    "previousRoom": event.previousRoom,
                    "room": event.room,
                    "vertretungstext": event.texts.text,
                    "cancelled": event.texts.cancelled,
                }
                for event in plan.events
            ]

            for i, event in enumerate(plaene_transformed):
                if event["lessons"] == "0":
                    plaene_transformed[i + 1]["vertretungstext"] += (
                        " " + plaene_transformed[i]["vertretungstext"]
                    )

            plaene_transformed_cleaned = [
                event for event in plaene_transformed if event["lessons"] != "0"
            ]

            vertretungsplaene.append(
                {
                    "first_plan": True if date == dates[0] else False,
                    "date": plan.date,
                    "version": plan.version,
                    "table": VertretungsplanTable(plaene_transformed_cleaned),
                }
            )

        logger.info(f"Rendering vertretungsplan template.")

        return render(
            request,
            self.template_name,
            context={"vertretungsplaene": vertretungsplaene},
        )
