from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from trainer import models


class TrainForm(forms.Form):
    deutsch = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "readonly": "readonly",
                "style": "width: 400px",
            }
        ),
        label="",
    )
    englisch = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Englischen Begriff eingeben.",
                "autocomplete": "off",
                "style": "width: 400px",
            }
        ),
        required=False,
        label="",
    )
    id = forms.IntegerField(widget=forms.HiddenInput())


class CreateVokabelForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=models.VokabelGroup.objects.order_by("-created").all(), initial=0
    )

    class Meta:
        model = models.Vokabel
        fields = ["deutsch", "englisch", "group"]
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "Diese Vokabel existiert bereits in dieser Gruppe.",
            }
        }
