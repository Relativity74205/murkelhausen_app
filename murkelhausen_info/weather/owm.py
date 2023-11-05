"""
API Documentations:
https://openweathermap.org/api/one-call-3
https://openweathermap.org/current

name = "Mülheim"
gps_lat = 51.418568
gps_lon = 6.884523
"""
from dataclasses import dataclass
from logging import getLogger
from django.conf import settings

import requests

from murkelhausen_info.weather.OWMOneCall import OWMOneCall

log = getLogger(__name__)


@dataclass
class City:
    name: str
    gps_lat: float
    gps_lon: float


@dataclass
class OWMConfig:
    url_weather: str
    url_onecall: str
    units: str
    api_key: str


MUELHEIM = City(name="Mülheim", gps_lat=51.418568, gps_lon=6.884523)


def query_one_call_api(city: City, owm_config: OWMConfig) -> OWMOneCall:
    data = _query_owm(
        owm_config.url_onecall, city, owm_config.api_key, owm_config.units
    )
    return OWMOneCall(**data)


def query_weather(city: City, owm_config: OWMConfig) -> dict:
    return _query_owm(
        owm_config.url_weather, city, owm_config.api_key, owm_config.units
    )


def _query_owm(url: str, city: City, api_key: str, units: str) -> dict:
    query_params: dict = {
        "lat": city.gps_lat,
        "lon": city.gps_lon,
        "appid": api_key,
        "units": units,
        "lang": "de",
    }
    r = requests.get(url, params=query_params)

    if r.status_code == 200:
        return_dict: dict = r.json()
        return return_dict
    elif r.status_code == 401:
        raise RuntimeError(f"Authentication error, {api_key=}.")
    else:
        raise RuntimeError(
            f"Query to openweatherapi one call api returned non 200 status code for city {city.name} with {api_key=}: "
            f"status_code: {r.status_code}"
            f"response_text: {r.text}"
        )


def get_weather_data_muelheim() -> OWMOneCall:
    owm_config = OWMConfig(
        url_weather="https://api.openweathermap.org/data/2.5/weather",
        url_onecall="https://api.openweathermap.org/data/3.0/onecall",
        units="metric",
        api_key=settings.OPENWEATHERMAP_API_KEY,
    )

    return query_one_call_api(MUELHEIM, owm_config)


a = 1
# print(json.dumps(data, indent=4))

# with open("owm.json", "w") as f:
#     json.dump(data, f, indent=4)

# def get_weather_map(layer: str, owm_settings: WeatherOWM):
#     """
#     https://openweathermap.org/api/weathermaps
#     https://github.com/google/maps-for-work-samples/blob/master/samples/maps/OpenWeatherMapLayer/OpenWeatherMapLayer.pdf
#     """
#     pass
#
#
# def query_air_pollution():
#     """
#     https://openweathermap.org/api/air-pollution
#     """
#     pass
