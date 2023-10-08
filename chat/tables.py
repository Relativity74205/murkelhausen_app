from django.utils.safestring import mark_safe
from django_tables2 import tables, LinkColumn, Column, DateTimeColumn, A

from chat import models


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


class ChatSystemTable(tables.Table):
    update = UpdateColumn(
        "chat:chatsystem_update",
        args=[A("id")],
        text="Ändern",
        verbose_name="Ändern",
        orderable=False,
    )
    delete = DeleteColumn(
        "chat:chatsystem_delete",
        args=[A("id")],
        text="Löschen",
        verbose_name="Löschen",
        orderable=False,
    )
    created = DateTimeColumn(format="d.m.Y H:i:s", verbose_name="Erstellt")

    class Meta:
        model = models.ChatSystem
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "name",
            "system_setup_text",
            "created",
        )
        order_by = "-created"
