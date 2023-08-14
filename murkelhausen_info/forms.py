from django import forms


class StationForm(forms.Form):
    Station = forms.ChoiceField(
        choices=((0, 'Lierberg'), (1, 'Kriegerstr.'), ),
    )
