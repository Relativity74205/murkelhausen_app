from django.urls import path

from . import views

app_name = "murkelhausen_info"
urlpatterns = [
    path("", views.start, name="start"),
    path("weather/", views.WeatherView.as_view(), name="weather"),
    path("weather_test", views.WeatherViewTest.as_view(), name="weather_test"),
    path("power/", views.power, name="power"),
    path("departures/", views.DepartureView.as_view(), name="show_departures"),
]
