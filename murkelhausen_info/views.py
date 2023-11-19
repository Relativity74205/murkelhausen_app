from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic.edit import FormMixin

from murkelhausen_info.forms import StationForm
from murkelhausen_info.mheg import get_muelltermine_for_home
from murkelhausen_info.mheg.main import get_muelltermine_for_this_week
from murkelhausen_info.ruhrbahn.main import get_departure_data, get_stations, STATIONS
from murkelhausen_info.tables import (
    DeparturesTable,
    WeatherTable,
    MuellTable,
    TemperatureTable,
)
from murkelhausen_info import weather


class IndexView(View):
    template_name = "murkelhausen_info/index.html"

    def get(self, request, *args, **kwargs):
        muell_termine = get_muelltermine_for_this_week()
        owm_data = weather.get_weather_data_muelheim()

        context = {
            "weather_data": owm_data,
            "muell_termine": muell_termine,
        }
        return render(request, self.template_name, context)


def power(request):
    return render(request, "murkelhausen_info/power.html")


class DepartureView(View, FormMixin):
    template_name = "murkelhausen_info/departures.html"

    @staticmethod
    def _get_data(station: str) -> list[dict]:
        station_id = get_stations().get_station_id(station, "Mülheim")

        departure_data = get_departure_data(station_id)
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

        return data

    def get(self, request, *args, **kwargs):
        station = self.request.session.get("station")
        if station is None:
            station = STATIONS[0]
        form = StationForm()
        form.initial["station"] = STATIONS.index(station)
        departure_data = self._get_data(station)
        table = DeparturesTable(departure_data[:20])
        table.paginate(page=request.GET.get("page", 1), per_page=20)
        return render(request, self.template_name, {"form": form, "table": table})

    def post(self, request, *args, **kwargs):
        form = StationForm(request.POST)
        if form.is_valid():
            station_position = form.cleaned_data["station"]
            station = STATIONS[int(station_position)]
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
        termine = get_muelltermine_for_home()
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
