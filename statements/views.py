import csv
import logging
from typing import Iterator

import pandas as pd
import plotly.express as px
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import UpdateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin


from . import models, forms, tables, filters
from .views_functions import parse_commerzbank_date, _add_keyword, _add_category, match_categories, \
    delete_set_categories


class StatementsView(SingleTableMixin, FilterView):
    model = models.CommerzbankStatement
    template_name = "statements/statements.html"
    table_class = tables.StatementsTable
    filterset_class = filters.StatementsFilter


class StartMatchingView(View):
    def post(self, request):
        match_categories()

        return HttpResponseRedirect(reverse_lazy('statements:statements'))


class DeleteMatchingView(View):
    def post(self, request):
        delete_set_categories()

        return HttpResponseRedirect(reverse_lazy('statements:statements'))


class CategoryDeleteView(generic.DeleteView):
    model = models.StatementCategory
    success_url = reverse_lazy('statements:categories')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class KeywordDeleteView(generic.DeleteView):
    model = models.StatementKeyword

    def get_success_url(self):
        return reverse_lazy('statements:category', kwargs={'category_id': self.object.category.id})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class StatementUpdateView(UpdateView):
    model = models.CommerzbankStatement
    form_class = forms.StatementUpdateForm
    template_name_suffix = "_update_form"
    success_url = reverse_lazy('statements:statements')


def import_statements(request):
    if request.method == "POST":
        form = forms.CSVUploadForm(request.POST, request.FILES)
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

                models.CommerzbankStatement.objects.create(
                    buchungstag=parse_commerzbank_date(row["Buchungstag"]),
                    wertstellung=parse_commerzbank_date(row["Wertstellung"]),
                    umsatzart=row["Umsatzart"],
                    buchungstext=row["Buchungstext"],
                    betrag=betrag,
                    waehrung=row["Währung"],
                    iban_auftraggeberkonto=row["IBAN Auftraggeberkonto"],
                )
            return HttpResponse(f"{count} rows have been imported.")  # TODO use django messages; len(csv_data) is not correct

    return render(request, "statements/import.html", {"form": forms.CSVUploadForm()})


def show_categories(request: HttpRequest):
    """View for managing categories and keywords."""
    categories = models.StatementCategory.objects.all()
    context = {
        "categories": categories,
        "add_category_form": forms.AddCategoryForm(),
        "add_category_message": request.session.get("add_category_message", ""),
    }

    if request.method == "POST":
        if request.POST.get("add_category"):
            _add_category(request, categories)
        return HttpResponseRedirect(request.path_info)

    request.session["add_category_message"] = ""
    return render(request, "statements/categories.html", context)


def show_category(request, category_id: int):
    category = models.StatementCategory.objects.filter(id=category_id).first()

    context = {
        "category": category,
        "add_keyword_form": forms.AddKeywordForm(),
        "add_keyword_message": request.session.get("add_keyword_message", ""),
    }

    if request.method == "POST":
        if request.POST.get("add_keyword"):
            _add_keyword(request, category)
        return HttpResponseRedirect(request.path_info)

    request.session["add_keyword_message"] = ""
    return render(request, "statements/category.html", context)


def plot_graph(request):
    positive_amounts = models.CommerzbankStatement.objects.filter(betrag__gt=0).annotate(
        month=TruncMonth('buchungstag')).values('month', 'category__name').annotate(sum_positive=Sum('betrag')).order_by('month')
    negative_amounts = models.CommerzbankStatement.objects.filter(betrag__lt=0).annotate(
        month=TruncMonth('buchungstag')).values('month', 'category__name').annotate(sum_negative=Sum('betrag')).order_by('month')
    df_negative = pd.DataFrame.from_records(negative_amounts)
    fig_negative = px.line(df_negative, x='month', y='sum_negative', color='category__name', title='Negative Amount per Month')

    # Convert plots to HTML
    plot_html = fig_negative.to_html(full_html=False)

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=list(negative_amounts.values_list('month', flat=True)), y=list(negative_amounts.values_list('sum_negative', flat=True)), name='Negative Amount'))
    # fig.add_trace(go.Scatter(x=list(positive_amounts.values_list('month', flat=True)), y=list(positive_amounts.values_list('sum_positive', flat=True)), name='Positive Amount'))
    # fig.update_layout(title='Negative and Positive Amount per Month', xaxis_title='Month', yaxis_title='Amount')
    # plot_html = fig.to_html(full_html=False)
    #
    # x_data = []
    # y_data = []
    # for amount in positive_amounts:
    #     x_data += [amount['month']]
    #     y_data += [amount['sum_positive']]
    # plot_div = plot([Scatter(x=x_data, y=y_data,
    #                     mode='lines', name='test',
    #                     opacity=0.8, marker_color='green')],
    #            output_type='div')

    # Pass the plot HTML to the template
    context = {
        'plot_html': plot_html
    }
    return render(request, "statements/graph.html", context=context)
