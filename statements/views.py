import csv
import logging
from typing import Iterator

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .models import CommerzbankStatement, StatementCategory, StatementKeyword
from .forms import CSVUploadForm, AddCategoryForm, AddKeywordForm, StatementForm
from .views_functions import parse_commerzbank_date, _add_keyword, _add_category


class StatementsView(generic.ListView):
    template_name = "statements/statements.html"
    context_object_name = "statements"

    def get_queryset(self):
        """Return the last five published questions."""
        return CommerzbankStatement.objects.all().order_by('id')


class CategoryDeleteView(generic.DeleteView):
    model = StatementCategory
    success_url = reverse_lazy('statements:categories')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class KeywordDeleteView(generic.DeleteView):
    model = StatementKeyword

    def get_success_url(self):
        return reverse_lazy('statements:category', kwargs={'category_id': self.object.category.id})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


# TODO check if replaced with update view?
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


def show_categories(request: HttpRequest):
    """View for managing categories and keywords."""
    categories = StatementCategory.objects.all()
    context = {
        "categories": categories,
        "add_category_form": AddCategoryForm(),
        "add_category_message": request.session.get("add_category_message", ""),
    }

    if request.method == "POST":
        if request.POST.get("add_category"):
            _add_category(request, categories)
        return HttpResponseRedirect(request.path_info)

    request.session["add_category_message"] = ""
    return render(request, "statements/categories.html", context)


def show_category(request, category_id: int):
    category = StatementCategory.objects.filter(id=category_id).first()

    context = {
        "category": category,
        "add_keyword_form": AddKeywordForm(),
        "add_keyword_message": request.session.get("add_keyword_message", ""),
    }

    if request.method == "POST":
        if request.POST.get("add_keyword"):
            _add_keyword(request, category)
        return HttpResponseRedirect(request.path_info)

    request.session["add_keyword_message"] = ""
    return render(request, "statements/category.html", context)
