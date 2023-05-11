import csv
import logging
from datetime import datetime, date
from typing import Iterator

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import CommerzbankStatement, StatementCategory, StatementKeyword
from .forms import CSVUploadForm, AddCategoryForm, AddKeywordForm, DeleteCategoryForm, StatementForm, DeleteKeywordForm


class StatementsView(generic.ListView):
    template_name = "statements/statements.html"
    context_object_name = "statements"

    def get_queryset(self):
        """Return the last five published questions."""
        return CommerzbankStatement.objects.all().order_by('id')


def show_statement(request, statement_id):
    statement = get_object_or_404(CommerzbankStatement, pk=statement_id)

    if request.method == 'POST':
        form = StatementForm(request.POST, instance=statement)
        if form.is_valid():
            stmt = form.save(commit=False)
            if stmt.category is not None:
                stmt.category_set_manually = True
            else:
                stmt.category_set_manually = False
            stmt.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = StatementForm(instance=statement)

    return render(request, 'statements/statement.html', {'form': form, 'statement': statement})


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

                CommerzbankStatement.objects.create(
                    buchungstag=parse_commerzbank_date(row["Buchungstag"]),
                    wertstellung=parse_commerzbank_date(row["Wertstellung"]),
                    umsatzart=row["Umsatzart"],
                    buchungstext=row["Buchungstext"],
                    betrag=betrag,
                    waehrung=row["Währung"],
                    iban_auftraggeberkonto=row["IBAN Auftraggeberkonto"],
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
        "add_category_message": request.session.get("add_category_message", ""),
        "delete_category_message": request.session.get("delete_category_message", ""),
    }

    if request.method == "POST":
        if request.POST.get("add_category"):
            _add_category(request, current_categories)
        elif request.POST.get("delete_category"):
            _delete_category(request)
        return HttpResponseRedirect(request.path_info)

    request.session["add_category_message"] = ""
    request.session["delete_category_message"] = ""
    return render(request, "statements/categories.html", context)


def show_category(request, category_id: int):
    category = StatementCategory.objects.filter(id=category_id).first()
    keyword_queryset = StatementKeyword.objects.filter(category=category).all()
    # Prepare the choices from the queryset
    choices = [(keyword.id, keyword.name) for keyword in keyword_queryset]

    # Pass the choices to the form
    delete_keyword_form = DeleteKeywordForm()
    delete_keyword_form.fields["Keyword"].choices = choices

    context = {
        "category": category,
        "add_keyword_form": AddKeywordForm(),
        "delete_keyword_form": delete_keyword_form,
        "add_keyword_message": request.session.get("add_keyword_message", ""),
        "delete_keyword_message": request.session.get("delete_keyword_message", ""),
    }

    if request.method == "POST":
        if request.POST.get("add_keyword"):
            _add_keyword(request, category)
        elif request.POST.get("delete_keyword"):
            _delete_keyword(request, category)
        return HttpResponseRedirect(request.path_info)

    request.session["add_keyword_message"] = ""
    request.session["delete_keyword_message"] = ""
    return render(request, "statements/category.html", context)


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


def _delete_keyword(request: HttpRequest, category: str):
    """Delete a keyword of a category from the database."""
    # TODO very dirty solution, cleanup needed
    # form = DeleteKeywordForm(request.POST)
    # if not form.is_valid():
    #     ...  # TODO add error handling
    # name = form.cleaned_data["Keyword"]
    StatementKeyword.objects.filter(category=category, id=request.POST["Keyword"][0]).delete()
    request.session["delete_keyword_message"] = f"Keyword for category {category} deleted."


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


def _delete_category(request: HttpRequest):
    """Delete a category from the database."""
    form = DeleteCategoryForm(request.POST)
    if not form.is_valid():
        ...  # TODO add error handling
    category = form.cleaned_data["Category"]
    StatementCategory.objects.filter(name=category).delete()
    request.session["delete_category_message"] = f"Category {category} deleted."
