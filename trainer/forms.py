from django import forms

from trainer.models import Vokabel


class TrainForm(forms.Form):
    class Meta:
        model = Vokabel
        fields = ['deutsch', 'englisch']
