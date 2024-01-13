import requests
from cachetools import TTLCache, cached

from murkelhausen_info.ruhrbahn.DepartureModel import DepartureModel
from murkelhausen_info.ruhrbahn.StationModel import StationModel

STATIONS = ("Lierberg", "Kriegerstr.")
URLS = {
    "stations": "https://ifa.ruhrbahn.de/stations",
    "routes": "https://ifa.ruhrbahn.de/routes",
    "locations": "https://ifa.ruhrbahn.de/locations",
    "stopFinder": "https://ifa.ruhrbahn.de/stopFinder/",
    "departure": "https://ifa.ruhrbahn.de/departure/",
    "trafficinfos": "https://ifa.ruhrbahn.de/trafficinfos",
    "tripRequest": "https://ifa.ruhrbahn.de/tripRequest/20015062/20015065/20230806/21:25/dep",
}


@cached(cache=TTLCache(maxsize=1, ttl=60))
def get_departure_data(station_id: str, _: int = None) -> DepartureModel:
    json_data = requests.get(URLS["departure"] + station_id).json()
    return DepartureModel(**json_data)


@cached(cache=TTLCache(maxsize=1, ttl=60 * 60 * 24))  # 1 day
def get_stations(_: int = None) -> StationModel:
    json_data = requests.get(URLS["stations"]).json()
    data = {"stations": json_data}
    return StationModel(**data)


def debug():
    stations = get_stations()
    station_id = stations.get_station_id("Hauptbahnhof", "Essen")
    departure_data = get_departure_data(station_id)
    # departures = departure_data.get_departure_list_per_line('125')
    departures = departure_data.get_departure_list()
    print(departures[0].planned_departure_time)


if __name__ == "__main__":
    debug()
