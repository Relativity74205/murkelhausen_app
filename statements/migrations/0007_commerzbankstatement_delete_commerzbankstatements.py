# Generated by Django 4.2.1 on 2023-05-11 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("statements", "0006_rename_keyword_statementkeyword_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommerzbankStatement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("buchungstag", models.DateField()),
                ("wertstellung", models.DateField()),
                ("umsatzart", models.CharField(max_length=256)),
                ("buchungstext", models.CharField(max_length=1024)),
                ("betrag", models.FloatField()),
                ("waehrung", models.CharField(max_length=8)),
                ("iban_auftraggeberkonto", models.CharField(max_length=32)),
                ("category_set_manually", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="statements.statementcategory",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="CommerzbankStatements",
        ),
    ]
