from django.forms import forms

from trainer import models


class AddVokabelForm(forms.ModelForm):
    class Meta:
        model = models.Vokabel
