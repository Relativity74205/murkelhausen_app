from django.urls import path

from . import views

app_name = "murkelhausen_info"
urlpatterns = [
    path("<str:station_name>/", views.show_departure, name="show_departure"),
    path("", views.show_departure, name="show_departures"),
]
