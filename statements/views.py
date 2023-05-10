import csv
import logging
from datetime import datetime, date
from typing import Iterator

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import CommerzbankStatements, StatementCategory, StatementKeyword
from .forms import CSVUploadForm, AddCategoryForm, AddKeywordForm


def index(request):
    context = {"statements": CommerzbankStatements.objects.all()}
    return render(request, "statements/index.html", context)


def render_statement(request, statement_id: int):
    statement = get_object_or_404(CommerzbankStatements, pk=statement_id)
    return render(request, "statements/statement.html", {"statement": statement})


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
    current_categories = StatementCategory.objects.all()
    context = {
        "categories": current_categories,
        "category_form": AddCategoryForm(),
        "keyword_form": AddKeywordForm(),
    }

    if request.method == "POST":
        if request.POST["add_category"]:
            form = AddCategoryForm(request.POST)
            if not form.is_valid():
                ...  # TODO add error handling

            new_category = form.cleaned_data["name"]
            if current_categories.filter(name=new_category).count() == 0:
                context["message"] = f"Category {new_category} added."
                StatementCategory.objects.create(name=new_category)
            else:
                context["message"] = "Category already exists."
                # render(request, "statements/categories.html", context)
        elif request.POST["add_keyword"]:
            form = AddKeywordForm(request.POST)
            if not form.is_valid():
                ...  # TODO add error handling

            if StatementKeyword.objects.filter(keyword=form.cleaned_data["keyword"], category=form.cleaned_data["category"]).count() == 0:
                StatementKeyword.objects.create(
                    keyword=form.cleaned_data["keyword"],
                    category=form.cleaned_data["category"],
                    is_regex=form.cleaned_data["is_regex"],
                )
            else:
                ...  # TODO add error handling

    return render(request, "statements/categories.html", context)
