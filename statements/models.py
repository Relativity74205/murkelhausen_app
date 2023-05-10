from django.db import models


class StatementCategory(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class StatementKeyword(models.Model):
    keyword = models.CharField(max_length=256)
    category = models.ForeignKey(StatementCategory, on_delete=models.SET_NULL, null=True, blank=True)
    is_regex = models.BooleanField(default=False)


class CommerzbankStatements(models.Model):
    buchungstag = models.DateField()
    wertstellung = models.DateField()
    umsatzart = models.CharField(max_length=256)
    buchungstext = models.CharField(max_length=1024)
    betrag = models.FloatField()
    waehrung = models.CharField(max_length=8)
    iban_auftraggeberkonto = models.CharField(max_length=32)
    category = models.ForeignKey(StatementCategory, on_delete=models.SET_NULL, null=True, blank=True)
