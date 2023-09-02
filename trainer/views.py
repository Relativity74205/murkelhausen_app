from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.views import generic

from trainer import models


class VokabelView(ListView):
    model = models.Vokabel
    template_name = "trainer/vokabeln.html"
    paginate_by = 10
    ordering = ['id']


class AddVokabelView(SuccessMessageMixin, generic.CreateView):
    model = models.Vokabel
    fields = ['deutsch', 'englisch']
    template_name_suffix = "_create_form"
    success_url = '/trainer/vokabel/'
    success_message = "%(deutsch)s erfolgreich hinzugefügt."


class UpdateVokabelView(SuccessMessageMixin, generic.UpdateView):
    model = models.Vokabel
    fields = ['deutsch', 'englisch']
    template_name_suffix = "_update_form"
    success_url = '/trainer/list/'
    success_message = "%(deutsch)s erfolgreich aktualisiert."


class DeleteVokabelView(SuccessMessageMixin, generic.DeleteView):
    model = models.Vokabel
    template_name_suffix = "_delete_form"
    success_url = '/trainer/list/'
    success_message = "Erfolgreich gelöscht."


def start(request):
    return render(request, "trainer/index.html")
