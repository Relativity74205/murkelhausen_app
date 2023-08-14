from django.urls import path

from . import views

app_name = "murkelhausen_info"
urlpatterns = [
    path("<str:station_name>/", views.DepartureView.as_view(), name="show_departure"),
    path("", views.DepartureView.as_view(), name="show_departures"),
]
