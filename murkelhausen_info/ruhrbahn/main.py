import json
from functools import lru_cache

import requests

from murkelhausen_info.ruhrbahn import URLS
from murkelhausen_info.ruhrbahn.DepartureModel import DepartureModel
from murkelhausen_info.ruhrbahn.StationModel import StationModel


def get_departure_data(station_id: str) -> DepartureModel:
    json_data = requests.get(URLS["departure"] + station_id).json()
    return DepartureModel(**json_data)


# TODO replace with ttl cache (https://github.com/tkem/cachetools)
@lru_cache()
def get_stations() -> StationModel:
    json_data = requests.get(URLS["stations"]).json()
    data = {"stations": json_data}
    return StationModel(**data)


stations = get_stations()
station_id = stations.get_station_id("Hauptbahnhof", "Essen")
departure_data = get_departure_data(station_id)
# departures = departure_data.get_departure_list_per_line('125')
departures = departure_data.get_departure_list()
print(departures[0].planned_departure_time)
