# Generated by Django 4.2.1 on 2023-05-09 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("statements", "0003_rename_commerzbankcategory_statementcategory_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="CommerzbankAuszug",
            new_name="CommerzbankStatements",
        ),
    ]
