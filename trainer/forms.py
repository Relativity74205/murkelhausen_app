from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from trainer import models


# TODO add crispy forms
# - https://django-crispy-forms.readthedocs.io/en/latest/layouts.html
# - https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
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
                "style": "width: 400px",
            }
        ),
        required=False,
        label="Wie heißt %(deutsch)s auf Englisch?",
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
