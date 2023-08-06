from django_filters import FilterSet, DateFromToRangeFilter, CharFilter, BooleanFilter, ModelChoiceFilter
from django_filters.widgets import DateRangeWidget, BooleanWidget

from . import models


class StatementsFilter(FilterSet):
    # category = MultipleChoiceFilter(choices=models.StatementCategory.objects.all().values_list('id', 'name'))
    buchungstag = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'type': 'date'}))
    buchungstext_contains = CharFilter(label="Buchungstext")
    category_set_manually = BooleanFilter(label="Manuell gesetzt", widget=BooleanWidget(attrs={'type': 'checkbox'}))
    category = ModelChoiceFilter(
        queryset=models.StatementCategory.objects.all(),
        label="Kategorie auswählen",
    )

    class Meta:
        model = models.CommerzbankStatement
        fields = {
            "buchungstext": ["icontains"],
            "category": ["exact"],
            "umsatzart": ["exact"],
            "buchungstag": ["exact"],
            "category_set_manually": ["exact"],
        }
