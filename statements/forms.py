from django import forms

from statements.models import StatementCategory, StatementKeyword


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select a CSV file')


class AddCategoryForm(forms.Form):
    name = forms.CharField(max_length=256)


class DeleteCategoryForm(forms.Form):
    Category = forms.ModelChoiceField(
        queryset=StatementCategory.objects.all(),
    )


class AddKeywordForm(forms.ModelForm):
    class Meta:
        model = StatementKeyword
        fields = "__all__"

        widgets = {
            'is_regex': forms.CheckboxInput(),
        }
