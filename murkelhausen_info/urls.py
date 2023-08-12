from django.urls import path

from . import views

app_name = "murkelhausen_info"
urlpatterns = [
    path("", views.FooView.as_view(), name="foo"),
]
