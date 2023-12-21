from django.urls import path

from . import views

app_name = "murkelhausen_info"
urlpatterns = [
    path("", views.IndexView.as_view(), name="start"),
    path("weather/", views.WeatherView.as_view(), name="weather"),
    path("power/", views.PowerView.as_view(), name="power"),
    path("departures/", views.DepartureView.as_view(), name="departures"),
    path(
        "vertretungsplan", views.VertretungsplanView.as_view(), name="vertretungsplan"
    ),
    path("muell/", views.MuellView.as_view(), name="muell"),
]
