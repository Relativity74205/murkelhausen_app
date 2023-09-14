from django import forms

from trainer.models import Vokabel


class TrainForm(forms.ModelForm):
    class Meta:
        model = Vokabel
        fields = ('deutsch', 'englisch', )

        widgets = {
            'deutsch': forms.TextInput(attrs={'readonly': 'readonly'}),
            'englisch': forms.TextInput(),
        }
