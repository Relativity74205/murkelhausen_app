from django.db import models


class VokabelGroup(models.Model):
    name = models.CharField(max_length=256)
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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    readonly_fields = ["created", "updated"]

    # TODO error message is bad: Vokabel with this Deutsch already exists.
    class Meta:
        unique_together = ("deutsch",)
