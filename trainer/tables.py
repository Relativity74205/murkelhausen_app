from django.conf import settings
from django.db.models import When, Case
from django.utils.safestring import mark_safe
from django_tables2 import tables, LinkColumn, A, DateTimeColumn, Column

from . import models


# TODO move to own common module
class DeleteColumn(LinkColumn):
    def render(self, record, value):
        return mark_safe('<i class="fas fa-times" style="color: red;"></i>')


# TODO move to own common module
class UpdateColumn(LinkColumn):
    def render(self, record, value):
        return mark_safe('<i class="fa-solid fa-pen-to-square"></i>')


# TODO move to own common module
class NumberColumn(Column):
    def render(self, value):
        return f"{value:.0f}"


class VokabelTable(tables.Table):
    update = UpdateColumn(
        "trainer:update",
        args=[A("id")],
        text="Ändern",
        verbose_name="Ändern",
        orderable=False,
        attrs={
            "td": {"style": "text-align: center"},
            "th": {"style": "text-align: center"},
        },
    )
    delete = DeleteColumn(
        "trainer:delete",
        args=[A("id")],
        text="Löschen",
        verbose_name="Löschen",
        orderable=False,
        attrs={
            "td": {"style": "text-align: center"},
            "th": {"style": "text-align: center"},
        },
    )
    group = Column(
        verbose_name="Gruppe",
    )
    total = Column(
        verbose_name="Anzahl Fragen",
        orderable=True,
        attrs={
            "td": {"style": "text-align: right"},
            "th": {"style": "text-align: right"},
        },
    )
    correct_percentage = NumberColumn(
        verbose_name="Richtig in %",
        attrs={
            "td": {"style": "text-align: right"},
            "th": {"style": "text-align: right"},
        },
    )
    correct_percentage_last = NumberColumn(
        verbose_name=f"Richtig in % (letzte {settings.TRAINER_LAST_N})",
        attrs={
            "td": {"style": "text-align: right"},
            "th": {"style": "text-align: right"},
        },
    )

    def order_total(self, queryset, is_descending):
        sorted_queryset = sorted(queryset, key=lambda x: x.total, reverse=is_descending)
        list_of_ids = [x.id for x in sorted_queryset]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(list_of_ids)])
        return queryset.filter(pk__in=list_of_ids).order_by(preserved), True

    def order_correct_percentage(self, queryset, is_descending):
        sorted_queryset = sorted(
            queryset, key=lambda x: x.correct_percentage, reverse=is_descending
        )
        list_of_ids = [x.id for x in sorted_queryset]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(list_of_ids)])
        return queryset.filter(pk__in=list_of_ids).order_by(preserved), True

    def order_correct_percentage_last(self, queryset, is_descending):
        sorted_queryset = sorted(
            queryset, key=lambda x: x.correct_percentage_last, reverse=is_descending
        )
        list_of_ids = [x.id for x in sorted_queryset]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(list_of_ids)])
        return queryset.filter(pk__in=list_of_ids).order_by(preserved), True

    class Meta:
        model = models.Vokabel
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "deutsch",
            "englisch",
            "group",
            "total",
            "correct_percentage",
            "correct_percentage_last",
        )
        order_by = ("deutsch",)
        attrs = {
            "class": "table table-hover",
            "thead": {
                "class": "table-light",
            },
        }


class VokabelGroupTable(tables.Table):
    update = UpdateColumn(
        "trainer:group_update",
        args=[A("id")],
        text="Ändern",
        verbose_name="Ändern",
        orderable=False,
    )
    delete = DeleteColumn(
        "trainer:group_delete",
        args=[A("id")],
        text="Löschen",
        verbose_name="Löschen",
        orderable=False,
    )
    created = DateTimeColumn(format="d.m.Y H:i:s", verbose_name="Erstellt")

    class Meta:
        model = models.VokabelGroup
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "name",
            "created",
        )
        order_by = "-created"
