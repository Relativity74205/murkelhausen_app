from django.urls import path, include
from django.views.generic import TemplateView

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
    path("garmin/", views.GarminView.as_view(), name="garmin"),
    path("beowulf/", views.SupersetBeowulf.as_view(), name="superset_beowulf"),
    path("fussball/", views.Fussball.as_view(), name="fussball"),
    path("get_superset_token/", views.get_superset_token, name="get_superset_token"),
    path("podcast_token/", views.get_podcast_token, name="podcast_token"),
]
