from datetime import timezone, datetime

from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView

from murkelhausen_info.forms import StationForm
from murkelhausen_info.ruhrbahn.main import get_stations, get_departure_data


# class FooView(TemplateView):
#     template_name = "murkelhausen_info/foo.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         stations = get_stations()
#         selected_station_name = self._get_selected_station()
#         station_id = stations.get_station_id(selected_station_name, "Mülheim")
#         departure_data = get_departure_data(station_id)
#         departures = departure_data.get_departure_list()
#
#         context["station_form"] = StationForm()
#         context["departures"] = departures
#         return context
#
#     def get_queryset(self):
#         pass
#
#     def post(self, request: HttpRequest, *args, **kwargs):
#         selected_station_name = self._get_selected_station(request)
#         print(f"{selected_station_name=}")
#
#         stations = get_stations()
#         station_id = stations.get_station_id(selected_station_name, "Mülheim")
#         departure_data = get_departure_data(station_id)
#         departures = departure_data.get_departure_list()
#
#         context = self.get_context_data()
#         context['departures'] = departures
#         # return self.render_to_response(context)
#
#         return HttpResponseRedirect(reverse_lazy('murkelhausen_info:foo'))
#         # else:
#         #     return HttpResponseRedirect(reverse_lazy('murkelhausen_info:foo'))
#
#     @staticmethod
#     def _get_selected_station(request: HttpRequest | None = None) -> str:
#         choices: dict[int, str] = dict(StationForm.base_fields['Station'].choices)
#         if request is None:
#             return choices[0]
#         else:
#             form = StationForm(request.POST)
#             # if form.is_valid():
#             selected_station_id = int(form.cleaned_data['Station'])
#             selected_station_name = choices[selected_station_id]
#             return selected_station_name


def show_departure(request: HttpRequest, station_name: str | None = None) -> HttpResponse:
    if station_name is None:
        station_name = "Lierberg"  # TODO replace with config value
    stations = get_stations()
    station_id = stations.get_station_id(station_name, "Mülheim")

    departure_data = get_departure_data(station_id)
    departures = departure_data.get_departure_list()

    context = {
        "selection_station": station_name,
        "departures": departures,
        # "station_form": StationForm(initial={'Station': 0}),
    }

    return render(request, "murkelhausen_info/foo.html", context)


def show_departures(request: HttpRequest):
    stations = get_stations()
    station_choices = _get_station_choices()

    if request.method == "POST":
        form = StationForm(request.POST)
        if form.is_valid():
            selected_station_id = int(form.cleaned_data['Station'])
        else:
            selected_station_id = 0
    else:
        selected_station_id = 0

    selected_station_name = station_choices[selected_station_id]
    station_id = stations.get_station_id(selected_station_name, "Mülheim")

    departure_data = get_departure_data(station_id)
    departures = departure_data.get_departure_list()

    context = {
        "selection_station": selected_station_name,
        "departures": departures,
        "station_form": StationForm(initial={'Station': selected_station_id}),
    }

    return render(request, "murkelhausen_info/foo.html", context)


def _get_station_choices() -> dict[int, str]:
    return dict(StationForm.base_fields['Station'].choices)
