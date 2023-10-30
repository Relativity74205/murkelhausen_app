from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormMixin

from murkelhausen_info.forms import StationForm
from murkelhausen_info.ruhrbahn.main import get_departure_data, get_stations, STATIONS
from murkelhausen_info.tables import DeparturesTable


def start(request):
    return render(request, "murkelhausen_info/index.html")


def weather(request):
    return render(request, "murkelhausen_info/weather.html")


def power(request):
    return render(request, "murkelhausen_info/power.html")


def show_departures(request):
    data = get_data()

    table = DeparturesTable(data)

    return render(request, "murkelhausen_info/departures.html", {"table": table})


def get_data(station: str):
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

    return data[:10]


class DepartureView(View, FormMixin):
    template_name = "murkelhausen_info/departures.html"

    def get(self, request, *args, **kwargs):
        station = self.request.session.get("station")
        if station is None:
            station = STATIONS[0]
        form = StationForm()
        form.initial["station"] = STATIONS.index(station)
        table = DeparturesTable(get_data(station))
        return render(request, self.template_name, {"form": form, "table": table})

    def post(self, request, *args, **kwargs):
        form = StationForm(request.POST)
        if form.is_valid():
            station_position = form.cleaned_data["station"]
            print(station_position)
            station = STATIONS[int(station_position)]
            self.request.session["station"] = station

        return HttpResponseRedirect(request.path_info)
