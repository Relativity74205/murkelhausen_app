from django.urls import path

from . import views

app_name = "statements"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.StatementView.as_view(), name="statement"),
    path("import/", views.import_statements, name="import"),
    path("categories/", views.categories, name="categories"),
]
