from django_tables2 import tables, Column


class DeparturesTable(tables.Table):
    linie = Column(verbose_name="Linie")
    departure_time = Column(verbose_name="Abfahrt")
    delay = Column(verbose_name="Verspätung")
    platform = Column(verbose_name="Gleis")
    richtung = Column(verbose_name="Richtung")

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
