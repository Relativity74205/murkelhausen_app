from django_tables2 import tables, LinkColumn, A

from . import models


class StatementsTable(tables.Table):
    Link = LinkColumn('statements:statement_update_form', args=[A('id')], text='Details')
    # row_attrs = {
    #     "onClick": lambda record: "document.location.href='/{0}';".format(record.id)
    # }

    class Meta:
        model = models.CommerzbankStatement
        template_name = "django_tables2/bootstrap.html"
        # fields = ("buchungstag", )
        exclude = ("id", "wertstellung", "waehrung", "iban_auftraggeberkonto", )
        order_by = ("buchungstag", "id", )
