from django import forms


class TrainForm(forms.Form):
    deutsch = forms.CharField(widget=forms.TextInput(attrs={"readonly": "readonly"}))
    englisch = forms.CharField(
        widget=forms.TextInput(),
        help_text="Englischen Begriff eingeben.",
        required=False,
    )
    id = forms.IntegerField(widget=forms.HiddenInput())
