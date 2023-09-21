from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models


class VokabelGroup(models.Model):
    name = models.CharField(
        max_length=256, error_messages={"unique": "Diese Gruppe existiert bereits."}
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name",)

    def __str__(self):
        return self.name


class Vokabel(models.Model):
    deutsch = models.CharField(max_length=256)
    englisch = models.CharField(max_length=256)
    group = models.ForeignKey(
        VokabelGroup, on_delete=models.SET_NULL, null=True, blank=True
    )
    results = ArrayField(models.BooleanField(), default=list)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    readonly_fields = ["created", "updated"]

    class Meta:
        unique_together = ("deutsch", "group")

    @property
    def total(self):
        return len(self.results)

    @property
    def count_correct(self):
        return sum(self.results)

    @property
    def count_wrong(self):
        return self.total - self.count_correct

    @property
    def correct_percentage(self):
        try:
            return self.count_correct / (self.count_correct + self.count_wrong) * 100
        except ZeroDivisionError:
            return 0

    @property
    def correct_percentage_last(self):
        last_n_results = self.results[-settings.TRAINER_LAST_N :]
        try:
            return sum(last_n_results) / len(last_n_results) * 100
        except ZeroDivisionError:
            return 0
