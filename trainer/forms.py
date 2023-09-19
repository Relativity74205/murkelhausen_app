from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from trainer import models


class VokabelGroupSelectForm(forms.Form):
    group = forms.ChoiceField(
        widget=forms.Select(attrs={"style": "width: 400px"}),
        choices=[],
        label="Wähle eine Gruppe aus.",
    )


class TrainForm(forms.Form):
    deutsch = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "readonly": "readonly",
                "style": "width: 400px; background-color: lightgrey",
            }
        ),
        label="",
    )
    englisch = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Englische Vokabel eingeben.",
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
        widget=forms.Select(),
        queryset=models.VokabelGroup.objects.order_by("-created").all(),
        initial=0,
        required=False,
    )

    class Meta:
        model = models.Vokabel
        fields = ["deutsch", "englisch", "group"]
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "Diese Vokabel existiert bereits in dieser Gruppe.",
            }
        }
