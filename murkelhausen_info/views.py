from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic.edit import FormMixin

from murkelhausen_info.forms import StationForm
from murkelhausen_info.ruhrbahn.main import get_departure_data, get_stations, STATIONS
from murkelhausen_info.tables import DeparturesTable, WeatherTable
from murkelhausen_info import weather


def start(request):
    return render(request, "murkelhausen_info/index.html")


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
        table = DeparturesTable(self._get_data(station))
        table.paginate(page=request.GET.get("page", 1), per_page=12)
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
    def _get_uv_index_category(uv_index: float) -> str:
        if uv_index < 3:
            return "keine bis gering"
        elif uv_index < 6:
            return "mittel"
        elif uv_index < 8:
            return "hoch"
        elif uv_index < 11:
            return "sehr hoch"
        else:
            return "extrem hoch"

    @staticmethod
    def _get_wind_direction(degrees: int) -> str:
        if degrees is None:
            return ""
        if degrees < 22.5:
            return "N"
        elif degrees < 67.5:
            return "NO"
        elif degrees < 112.5:
            return "O"
        elif degrees < 157.5:
            return "SO"
        elif degrees < 202.5:
            return "S"
        elif degrees < 247.5:
            return "SW"
        elif degrees < 292.5:
            return "W"
        elif degrees < 337.5:
            return "NW"
        else:
            return "N"

    def _get_weather_table_data(self, owm_data: weather.OWMOneCall) -> list[dict]:
        rain_data = (
            f"{owm_data.current.rain.get('1h', None)} mm/h"
            if owm_data.current.rain is not None
            else None
        )
        snow_data = (
            f"{owm_data.current.snow.get('1h', None)} mm/h"
            if owm_data.current.snow is not None
            else None
        )
        # weather_states = []
        # for weather_state in owm_data.current.weather:
        #     weather_states.append(f"{weather_state}")
        data = {
            "Temperatur": f"{owm_data.current.temp} °C",
            "Gefühlt": f"{owm_data.current.feels_like} °C",
            "Luftfeuchtigkeit": f"{owm_data.current.humidity} %",
            "Taupunkt": f"{owm_data.current.dew_point} °C",
            "UV Index": (
                f"{owm_data.current.uvi} ({self._get_uv_index_category(owm_data.current.uvi)})",
                mark_safe(
                    "<a href='https://de.wikipedia.org/wiki/UV-Index' target='_blank'>0 - 11+</a>"
                ),
            ),
            "Bewölkung": f"{owm_data.current.clouds} %",
            "Sichtweite": (f"{owm_data.current.visibility} m", "max. 10 km"),
            "Regen": rain_data,
            "Schnee": snow_data,
            "Windgeschwindigkeit": f"{owm_data.current.wind_speed} m/s",
            "Windrichtung": (
                self._get_wind_direction(owm_data.current.wind_deg),
                "aus welcher Richtung der Wind kommt",
            ),
            "Sonnenaufgang": f"{owm_data.current.sunrise_timestamp}",
            "Sonnenuntergang": f"{owm_data.current.sunset_timestamp}",
        }

        transformed_data = []
        for attribute, value in data.items():
            if type(value) is tuple:
                transformed_data.append(
                    {"attribute": attribute, "value": value[0], "comment": value[1]}
                )
            else:
                transformed_data.append(
                    {"attribute": attribute, "value": value, "comment": ""}
                )
        return transformed_data

    def get(self, request, *args, **kwargs):
        owm_data = weather.get_weather_data_muelheim()
        weather_table = WeatherTable(self._get_weather_table_data(owm_data))
        return render(
            request,
            "murkelhausen_info/weather.html",
            {"weather_data": owm_data, "weather_table": weather_table},
        )
