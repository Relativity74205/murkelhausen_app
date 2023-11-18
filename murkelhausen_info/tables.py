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
            return "background-color: orange;"
        if value > 1:
            return "background-color: yellow;"
        if value > 0:
            return "background-color: lightyellow;"
        else:
            return "background-color: white;"


class WeatherTable(tables.Table):
    attribute = Column(verbose_name="")
    current = Column(verbose_name="aktuell")
    forecast_today = Column(verbose_name="Vorhersage für heute")
    forecast_tomorrow = Column(verbose_name="Vorhersage für morgen")
    comment = Column(verbose_name="Kommentar", default=" ")

    class Meta:
        orderable = False
        template_name = "django_tables2/bootstrap5.html"


class TemperatureTable(tables.Table):
    zeitpunkt = Column(verbose_name="")
    wert = Column(verbose_name="")

    class Meta:
        orderable = False
        template_name = "django_tables2/table.html"
        show_header = False


class MuellTable(tables.Table):
    day = Column(verbose_name="Datum")
    art = Column(verbose_name="Tonne")
    delta_days = Column(verbose_name="in Tagen")

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
        row_attrs = {
            "style": lambda record: MuellTable._get_background_color(
                record["delta_days"]
            )
        }

    @staticmethod
    def _get_background_color(value):
        if value == 0:
            return "background-color: orange;"
        elif value == 1:
            return "background-color: yellow;"
        else:
            return "background-color: white;"
