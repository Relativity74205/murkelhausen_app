from django.shortcuts import render
from django.views.generic import ListView

from murkelhausen_info.forms import StationForm
from murkelhausen_info.ruhrbahn.DepartureModel import DepartureListItem
from murkelhausen_info.ruhrbahn.main import get_stations, get_departure_data


class DepartureView(ListView):
    model = DepartureListItem
    template_name = "murkelhausen_info/departures.html"
    paginate_by = 10
    station_name = "Lierberg"

    def get_queryset(self, **kwargs):
        station_name_param = self.kwargs.get("station_name", None)
        if station_name_param is not None:
            self.station_name = station_name_param

        stations = get_stations()
        station_id = stations.get_station_id(self.station_name, "Mülheim")

        departure_data = get_departure_data(station_id)
        departures = departure_data.get_departure_list()

        return departures

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selection_station"] = self.station_name
        return context


def _get_station_choices() -> dict[int, str]:
    return dict(StationForm.base_fields["Station"].choices)


def start(request):
    return render(request, "murkelhausen_info/index.html")


def weather(request):
    return render(request, "murkelhausen_info/weather.html")


def power(request):
    return render(request, "murkelhausen_info/power.html")
