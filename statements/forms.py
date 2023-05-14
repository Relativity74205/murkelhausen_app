from django import forms

from . import models


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select a CSV file')


class AddCategoryForm(forms.Form):
    name = forms.CharField(max_length=256)


class DeleteCategoryForm(forms.Form):
    Category = forms.ModelChoiceField(
        queryset=models.StatementCategory.objects.all(),
    )


class AddKeywordForm(forms.ModelForm):
    class Meta:
        model = models.StatementKeyword
        fields = ["name", "is_regex"]

        widgets = {
            'is_regex': forms.CheckboxInput(),
        }


class DeleteKeywordForm(forms.Form):
    Keyword = forms.ChoiceField(choices=[])


class StatementUpdateForm(forms.ModelForm):
    class Meta:
        model = models.CommerzbankStatement
        fields = '__all__'  # Replace with the specific fields you want to include in the form
        widgets = {
            'buchungstext': forms.Textarea(attrs={'class': 'custom-input'}),
        }
