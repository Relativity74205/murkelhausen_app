from django_filters import (
    FilterSet,
    DateFromToRangeFilter,
    CharFilter,
    BooleanFilter,
    ModelChoiceFilter,
)
from django_filters.widgets import DateRangeWidget, BooleanWidget

from . import models


class VokabelTableFilter(FilterSet):
    deutsch = CharFilter(label="Deutsche Vokabel", lookup_expr="icontains")
    englisch = CharFilter(label="Englische Vokabel", lookup_expr="icontains")
    group = ModelChoiceFilter(
        queryset=models.VokabelGroup.objects.all(),
        label="Gruppe auswählen",
    )

    class Meta:
        model = models.Vokabel
        fields = ["deutsch", "englisch"]
