from django_tables2 import tables

from . import models


class StatementsTable(tables.Table):
    class Meta:
        model = models.CommerzbankStatement
        template_name = "django_tables2/bootstrap.html"
        # fields = ("buchungstag", )
        exclude = ("id", "wertstellung", "waehrung", "iban_auftraggeberkonto", )
