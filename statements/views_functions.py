from datetime import date, datetime

from django.http import HttpRequest

from statements.forms import AddKeywordForm, AddCategoryForm
from statements.models import StatementKeyword, StatementCategory


def parse_commerzbank_date(date_string: str) -> date:
    try:
        return datetime.strptime(date_string, '%d.%m.%Y').date()
    except ValueError:
        new_date_string = f"01.{int(date_string[3:5])+1}.{date_string[6:]}"
        return datetime.strptime(new_date_string, '%d.%m.%Y').date()


def _add_keyword(request: HttpRequest, category: str):
    """Add a new keyword to the database."""
    form = AddKeywordForm(request.POST)
    if not form.is_valid():
        ...  # TODO add error handling
    name = form.cleaned_data["name"]
    if StatementKeyword.objects.filter(name=name, category=category).count() == 0:
        request.session["add_keyword_message"] = f"Keyword {name} for category {category} added."
        StatementKeyword.objects.create(
            name=name,
            category=category,
            is_regex=form.cleaned_data["is_regex"],
        )
    else:
        request.session["add_keyword_message"] = f"Keyword {name} for category {category} already exists."


def _add_category(request: HttpRequest, current_categories):
    """Add a new category to the database."""
    form = AddCategoryForm(request.POST)
    if not form.is_valid():
        ...  # TODO add error handling
    name = form.cleaned_data["name"]
    if current_categories.filter(name=name).count() == 0:
        request.session["add_category_message"] = f"Category {name} added."
        StatementCategory.objects.create(name=name)
    else:
        request.session["add_category_message"] = f"Category {name} already exists."
