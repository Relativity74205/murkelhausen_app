from django.urls import path

from . import views

app_name = "statements"
urlpatterns = [
    path("", views.StatementsView.as_view(), name="statements"),
    path("<int:statement_id>/", views.statement, name="statement"),
    path("import/", views.import_statements, name="import"),
    path("category/", views.categories, name="categories"),
    path("category/<int:category_id>/", views.show_category, name="category"),
]
