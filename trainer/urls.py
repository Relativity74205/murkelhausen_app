from django.urls import path

from . import views

app_name = "trainer"
urlpatterns = [
    path("", views.start, name="start"),
    path("list/", views.VokabelView.as_view(), name="list"),
    path("vokabel/", views.AddVokabelView.as_view(), name="add"),
    path("vokabel/<int:pk>/", views.UpdateVokabelView.as_view(), name="update"),
    path("vokabel/<int:pk>/delete", views.DeleteVokabelView.as_view(), name="delete"),
]
