# Generated by Django 4.2.5 on 2023-09-17 08:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trainer", "0005_alter_vokabelgroup_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="vokabel",
            name="count_correct",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="vokabel",
            name="count_wrong",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="vokabel",
            name="results",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.BooleanField(), default=list, size=None
            ),
        ),
    ]
