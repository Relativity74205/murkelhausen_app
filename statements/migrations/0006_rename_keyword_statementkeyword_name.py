# Generated by Django 4.2.1 on 2023-05-10 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("statements", "0005_alter_statementkeyword_is_regex"),
    ]

    operations = [
        migrations.RenameField(
            model_name="statementkeyword",
            old_name="keyword",
            new_name="name",
        ),
    ]
