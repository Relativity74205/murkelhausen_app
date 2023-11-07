from django import forms

from murkelhausen_info.ruhrbahn.main import STATIONS


class StationForm(forms.Form):
    station = forms.ChoiceField(
        choices=[(i, station) for i, station in enumerate(STATIONS)],
        label="Station",
    )
