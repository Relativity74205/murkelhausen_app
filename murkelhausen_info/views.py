from datetime import timezone, datetime

from django.views.generic import DetailView, TemplateView

from murkelhausen_info.ruhrbahn.main import get_stations, get_departure_data


class FooView(TemplateView):
    template_name = "murkelhausen_info/foo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["now"] = datetime.now()
        stations = get_stations()
        station_id = stations.get_station_id("Hauptbahnhof", "Essen")
        departure_data = get_departure_data(station_id)
        # departures = departure_data.get_departure_list_per_line('125')
        departures = departure_data.get_departure_list()
        context["departures"] = departures
        return context

    def get_queryset(self):
        pass
