from django import forms

from trainer import models


# TODO add crispy forms
# - https://django-crispy-forms.readthedocs.io/en/latest/layouts.html
# - https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
class TrainForm(forms.Form):
    deutsch = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))
    englisch = forms.CharField(
        widget=forms.TextInput(attrs={"autocomplete": "off", "size": 40}),
        label="Englischen Begriff eingeben.",
        required=False,
    )
    id = forms.IntegerField(widget=forms.HiddenInput())


class CreateVokabelForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=models.VokabelGroup.objects.order_by("-created").all(), initial=0
    )

    class Meta:
        model = models.Vokabel
        fields = ["deutsch", "englisch", "group"]
