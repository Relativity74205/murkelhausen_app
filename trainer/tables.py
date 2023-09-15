from django.utils.safestring import mark_safe
from django_tables2 import tables, LinkColumn, A, Column

from . import models


class DeleteColumn(LinkColumn):
    def render(self, record, value):
        return mark_safe('<i class="fas fa-times" style="color: red;"></i>')


class UpdateColumn(LinkColumn):
    def render(self, record, value):
        return mark_safe('<i class="fa-solid fa-pen-to-square"></i>')


class VokabelTable(tables.Table):
    update = UpdateColumn(
        "trainer:update", args=[A("id")], text="Ändern", verbose_name="Ändern"
    )
    delete = DeleteColumn(
        "trainer:delete", args=[A("id")], text="Löschen", verbose_name="Löschen"
    )

    class Meta:
        model = models.Vokabel
        template_name = "django_tables2/bootstrap.html"
        fields = ("deutsch", "englisch")
        order_by = ("deutsch",)
