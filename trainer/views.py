from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, FormView
from django.views import generic, View

from trainer import models, forms
from trainer.forms import TrainForm


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


class TrainView(View):
    def get(self, request, *args, **kwargs):

        vokabel = models.Vokabel.objects.order_by('?').first()
        context = {
            "deutsch": vokabel.deutsch,
            "englisch": vokabel.englisch,
        }
        return render(request, "trainer/train.html", context)

    def post(self, request, **kwargs):
        form = request.POST.dict()
        answer = form.get('answer')
        correct_answer = form.get('correct_answer')
        if answer == correct_answer:
            msg = f"Deine Antwort ({answer}) ist richtig."
        else:
            msg = f"Deine Antwort ({answer}) ist falsch. Die richtige Antwort wäre {correct_answer} gewesen."
        messages.add_message(request, messages.INFO, msg)

        return HttpResponseRedirect(request.path_info)


def start(request):
    return render(request, "trainer/index.html")
