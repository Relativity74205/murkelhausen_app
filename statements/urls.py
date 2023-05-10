from django.urls import path

from . import views

app_name = "statements"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:statement_id>/", views.render_statement, name="statement"),
    path("import/", views.import_statements, name="import"),
    path("categories/", views.categories, name="categories"),
]
