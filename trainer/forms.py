from django import forms


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
