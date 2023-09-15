from django.urls import path

from . import views

app_name = "trainer"
urlpatterns = [
    path("", views.start, name="start"),
    path("train/", views.TrainView.as_view(), name="train"),
    path("vokabel/", views.VokabelView.as_view(), name="list"),
    path("vokabel/add/", views.AddVokabelView.as_view(), name="add"),
    path("vokabel/<int:pk>/", views.UpdateVokabelView.as_view(), name="update"),
    path("vokabel/<int:pk>/delete", views.DeleteVokabelView.as_view(), name="delete"),
    path("vokabel_group/", views.VokabelGroupView.as_view(), name="group_list"),
    path("vokabel_group/add/", views.AddVokabelGroupView.as_view(), name="group_add"),
    path(
        "vokabel_group/<int:pk>/",
        views.UpdateVokabelGroupView.as_view(),
        name="group_update",
    ),
    path(
        "vokabel_group/<int:pk>/delete",
        views.DeleteVokabelGroupView.as_view(),
        name="group_delete",
    ),
]
