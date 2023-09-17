from django.conf import settings
from django.utils.safestring import mark_safe
from django_tables2 import tables, LinkColumn, A, DateTimeColumn, Column

from . import models


class DeleteColumn(LinkColumn):
    def render(self, record, value):
        return mark_safe('<i class="fas fa-times" style="color: red;"></i>')


class UpdateColumn(LinkColumn):
    def render(self, record, value):
        return mark_safe('<i class="fa-solid fa-pen-to-square"></i>')


class NumberColumn(Column):
    def render(self, value):
        return f"{value:.0f}"


class VokabelTable(tables.Table):
    update = UpdateColumn(
        "trainer:update", args=[A("id")], text="Ändern", verbose_name="Ändern"
    )
    delete = DeleteColumn(
        "trainer:delete", args=[A("id")], text="Löschen", verbose_name="Löschen"
    )
    group = Column(verbose_name="Gruppe")
    total = Column(verbose_name="Anzahl Fragen")
    correct_percentage = NumberColumn(verbose_name="Richtig in %")
    correct_percentage_last = NumberColumn(
        verbose_name=f"Richtig in % (letzte {settings.TRAINER_LAST_N})"
    )

    class Meta:
        model = models.Vokabel
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "deutsch",
            "englisch",
            "group",
            "total",
            "correct_percentage",
            "correct_percentage_last",
        )
        order_by = ("deutsch",)


class VokabelGroupTable(tables.Table):
    update = UpdateColumn(
        "trainer:group_update", args=[A("id")], text="Ändern", verbose_name="Ändern"
    )
    delete = DeleteColumn(
        "trainer:group_delete", args=[A("id")], text="Löschen", verbose_name="Löschen"
    )
    created = DateTimeColumn(format="d.m.Y H:i:s", verbose_name="Erstellt")

    class Meta:
        model = models.Vokabel
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "name",
            "created",
        )
        order_by = "-created"
