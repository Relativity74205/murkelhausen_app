from django.urls import path

from . import views

app_name = "murkelhausen_info"
urlpatterns = [
    path("", views.start, name="start"),
    path("departures/", views.DepartureView.as_view(), name="show_departures"),
    path(
        "departures/<str:station_name>/",
        views.DepartureView.as_view(),
        name="show_departure",
    ),
]
