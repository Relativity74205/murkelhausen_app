from django.db import models


class Vokabel(models.Model):
    deutsch = models.CharField(max_length=256)
    englisch = models.CharField(max_length=256)
