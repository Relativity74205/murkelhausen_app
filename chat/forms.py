from django import forms

from chat import models


class QAForm(forms.Form):
    input = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "GPT fragen.",
                "autocomplete": "off",
                "style": "width: 400px",
            }
        ),
        label="",
    )
    system = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=models.ChatSystem.objects.order_by("-created").all(),
        required=False,
    )
