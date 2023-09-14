from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, FormView
from django.views import generic, View
from django.views.generic.edit import ModelFormMixin

from trainer import models, forms
from trainer.forms import TrainForm


class VokabelView(ListView):
    model = models.Vokabel
    template_name = "trainer/vokabeln.html"
    paginate_by = 10
    ordering = ["id"]


class AddVokabelView(SuccessMessageMixin, generic.CreateView):
    model = models.Vokabel
    fields = ["deutsch", "englisch"]
    template_name_suffix = "_create_form"
    success_url = "/trainer/vokabel/"
    success_message = "%(deutsch)s erfolgreich hinzugefügt."


class UpdateVokabelView(SuccessMessageMixin, generic.UpdateView):
    model = models.Vokabel
    fields = ["deutsch", "englisch"]
    template_name_suffix = "_update_form"
    success_url = "/trainer/list/"
    success_message = "%(deutsch)s erfolgreich aktualisiert."


class DeleteVokabelView(SuccessMessageMixin, generic.DeleteView):
    model = models.Vokabel
    template_name_suffix = "_delete_form"
    success_url = "/trainer/list/"
    success_message = "Erfolgreich gelöscht."


class TrainView(View):
    @staticmethod
    def _retrieve_from_session(request, key: str) -> str | None:
        if key in request.session:
            return request.session.pop(key)

    def get(self, request, *args, **kwargs):
        vokabel = models.Vokabel.objects.order_by("?").first()

        given_answer = self._retrieve_from_session(request, "given_answer")
        correct_answer = self._retrieve_from_session(request, "correct_answer")
        correctly = self._retrieve_from_session(request, "correctly")

        context = {
            "vokabel": vokabel,
            "given_answer": given_answer,
            "correct_answer": correct_answer,
            "answered_correctly": correctly,
        }
        return render(request, "trainer/train.html", context)

    def post(self, request, **kwargs):
        form = request.POST.dict()
        answer = form.get("answer")
        vokabel_id = form.get("vokabel_id")
        vokabel = models.Vokabel.objects.get(id=vokabel_id)

        request.session["given_answer"] = vokabel.deutsch
        request.session["correct_answer"] = vokabel.englisch
        request.session["correctly"] = answer == vokabel.englisch

        return HttpResponseRedirect(request.path_info)


def start(request):
    return render(request, "trainer/index.html")
