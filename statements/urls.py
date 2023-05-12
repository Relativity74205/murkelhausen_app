from django.urls import path

from . import views
from .views import CategoryDeleteView, KeywordDeleteView

app_name = "statements"
urlpatterns = [
    path("", views.StatementsView.as_view(), name="statements"),
    path("<int:statement_id>/", views.show_statement, name="statement"),
    path("import/", views.import_statements, name="import"),
    path("category/", views.show_categories, name="categories"),
    path("category/<int:category_id>/", views.show_category, name="category"),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('category/<int:category_id>/<int:pk>/delete', KeywordDeleteView.as_view(), name='keyword-delete'),
]
