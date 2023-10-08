from django import forms


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
