# Generated by Django 4.2.5 on 2023-09-16 08:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("trainer", "0003_alter_vokabel_unique_together_vokabelgroup_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="vokabelgroup",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="vokabelgroup",
            name="updated",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
