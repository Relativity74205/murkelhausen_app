from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    path("", views.start, name="start"),
    path("qa/", views.QAView.as_view(), name="qa"),
]
