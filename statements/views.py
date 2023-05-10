import csv
import logging
from datetime import datetime, date
from typing import Iterator

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import CommerzbankStatements, StatementCategory, StatementKeyword
from .forms import CSVUploadForm, AddCategoryForm, AddKeywordForm, DeleteCategoryForm


# def index(request):
#     context = {"statements": CommerzbankStatements.objects.all()}
#     return render(request, "statements/index.html", context)
class IndexView(generic.ListView):
    template_name = "statements/index.html"
    context_object_name = "statements"

    def get_queryset(self):
        """Return the last five published questions."""
        return CommerzbankStatements.objects.all()


class StatementView(generic.DetailView):
    model = CommerzbankStatements
    template_name = "statements/statement.html"


def parse_commerzbank_date(date_string: str) -> date:
    try:
        return datetime.strptime(date_string, '%d.%m.%Y').date()
    except ValueError:
        new_date_string = f"01.{int(date_string[3:5])+1}.{date_string[6:]}"
        return datetime.strptime(new_date_string, '%d.%m.%Y').date()


def import_statements(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            csv_data: Iterator[dict] = csv.DictReader(decoded_file.splitlines(), delimiter=';')
            count = 0
            for row in csv_data:
                count += 1
                try:
                    betrag = float(row["Betrag"].replace(",", "."))
                except ValueError:
                    logging.exception(f"Could not parse {row['Betrag']}.")  # TODO how does logging work in django?
                    betrag = 0.0

                CommerzbankStatements.objects.create(
                    buchungstag=parse_commerzbank_date(row["Buchungstag"]),
                    wertstellung=parse_commerzbank_date(row["Wertstellung"]),
                    umsatzart=row["Umsatzart"],
                    buchungstext=row["Buchungstext"],
                    betrag=betrag,
                    waehrung=row["Währung"],
                    iban_auftraggeberkonto=["IBAN Auftraggeberkonto"],
                )
            return HttpResponse(f"{count} rows have been imported.")  # TODO use django messages; len(csv_data) is not correct

    return render(request, "statements/import.html", {"form": CSVUploadForm()})


def categories(request: HttpRequest):
    """View for managing categories and keywords."""
    current_categories = StatementCategory.objects.all()
    context = {
        "categories": current_categories,
        "add_category_form": AddCategoryForm(),
        "delete_category_form": DeleteCategoryForm(),
        "add_keyword_form": AddKeywordForm(),
        "add_category_message": request.session.get("add_category_message", ""),
        "delete_category_message": request.session.get("delete_category_message", ""),
        "add_keyword_message": request.session.get("add_keyword_message", ""),
        "delete_keyword_message": request.session.get("delete_keyword_message", ""),
        "matching_message": request.session.get("start_matching_message", ""),
    }

    if request.method == "POST":
        if request.POST.get("add_category"):
            _add_category(request, current_categories)
        elif request.POST.get("add_keyword"):
            _add_keyword(request)
        elif request.POST.get("delete_category"):
            _delete_category(request)
        return HttpResponseRedirect(request.path_info)

    request.session["add_category_message"] = ""
    request.session["delete_category_message"] = ""
    request.session["add_keyword_message"] = ""
    request.session["delete_keyword_message"] = ""
    request.session["matching_message"] = ""
    return render(request, "statements/categories.html", context)


def _add_keyword(request: HttpRequest):
    """Add a new keyword to the database."""
    form = AddKeywordForm(request.POST)
    if not form.is_valid():
        ...  # TODO add error handling
    new_keyword = form.cleaned_data["name"]
    category = form.cleaned_data["category"]
    if StatementKeyword.objects.filter(keyword=new_keyword, category=category).count() == 0:
        request.session["add_keyword_message"] = f"Keyword {new_keyword} for {category=} added."
        StatementKeyword.objects.create(
            keyword=new_keyword,
            category=category,
            is_regex=form.cleaned_data["is_regex"],
        )
    else:
        request.session["add_keyword_message"] = f"Keyword {new_keyword} for {category=} already exists."


def _add_category(request: HttpRequest, current_categories):
    """Add a new category to the database."""
    form = AddCategoryForm(request.POST)
    if not form.is_valid():
        ...  # TODO add error handling
    new_category = form.cleaned_data["name"]
    if current_categories.filter(name=new_category).count() == 0:
        request.session["add_category_message"] = f"Category {new_category} added."
        StatementCategory.objects.create(name=new_category)
    else:
        request.session["add_category_message"] = f"Category {new_category} already exists."


def _delete_category(request: HttpRequest):
    """Delete a category from the database."""
    form = DeleteCategoryForm(request.POST)
    if not form.is_valid():
        ...  # TODO add error handling
    category = form.cleaned_data["Category"]
    StatementCategory.objects.filter(name=category).delete()
    request.session["delete_category_message"] = f"Category {category} deleted."
