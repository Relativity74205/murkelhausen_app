from django_filters import FilterSet, DateFromToRangeFilter, BooleanFilter
from django_filters.widgets import DateRangeWidget, BooleanWidget

from . import models


class StatementsFilter(FilterSet):
    # category = MultipleChoiceFilter(choices=models.StatementCategory.objects.all().values_list('id', 'name'))
    buchungstag = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = models.CommerzbankStatement
        fields = {
            "buchungstext": ["icontains"],
            "category": ["exact"],
            "umsatzart": ["exact"],
            "buchungstag": ["exact"],
            "category_set_manually": ["exact"],
        }
