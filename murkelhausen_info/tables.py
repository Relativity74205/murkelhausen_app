from django_tables2 import tables, Column


class DelayColumn(Column):
    def render(self, record, value):
        if value == 0:
            return ""
        else:
            return value


class DeparturesTable(tables.Table):
    linie = Column(verbose_name="Linie")
    departure_time = Column(verbose_name="Abfahrt")
    delay = DelayColumn(verbose_name="Verspätung")
    platform = Column(verbose_name="Gleis")
    richtung = Column(verbose_name="Richtung")

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
        row_attrs = {
            "style": lambda record: DeparturesTable._get_background_color(
                record["delay"]
            )
        }

    @staticmethod
    def _get_background_color(value):
        if value >= 5:
            return "background-color: lightred;"
        if value > 1:
            return "background-color: yellow;"
        if value > 0:
            return "background-color: lightyellow;"
        else:
            return "background-color: white;"


class WeatherTable(tables.Table):
    attribute = Column(verbose_name="")
    current = Column(verbose_name="aktuell")
    forecast = Column(verbose_name="Vorhersage")
    comment = Column(verbose_name="Kommentar")

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
