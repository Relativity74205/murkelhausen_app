from django_filters import (
    FilterSet,
    CharFilter,
    ModelChoiceFilter,
)

from . import models


class ChatSystemFilter(FilterSet):
    name = CharFilter(label="System Name", lookup_expr="icontains")
    system_setup_text = CharFilter(
        label="Beschreibung des Systems", lookup_expr="icontains"
    )

    class Meta:
        model = models.ChatSystem
        fields = ["name", "system_setup_text"]
