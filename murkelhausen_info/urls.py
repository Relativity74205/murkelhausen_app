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
    path(
        "foo",
        views.Foo.as_view(),
        name="foo",
    ),
    path("get_superset_token/", views.get_superset_token, name="get_superset_token"),
]
