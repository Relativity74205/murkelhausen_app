from django_filters import (
    FilterSet,
    CharFilter,
    ModelChoiceFilter,
)

from . import models


class VokabelTableFilter(FilterSet):
    deutsch = CharFilter(label="Deutsche Vokabel", lookup_expr="icontains")
    englisch = CharFilter(label="Englische Vokabel", lookup_expr="icontains")
    group = ModelChoiceFilter(
        queryset=models.VokabelGroup.objects.order_by("-created").all(),
        label="Gruppe auswählen",
    )

    class Meta:
        model = models.Vokabel
        fields = ["deutsch", "englisch"]
