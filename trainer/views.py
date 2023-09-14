from dataclasses import dataclass

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, FormView
from django.views import generic, View
from django.views.generic.edit import ModelFormMixin
from pydantic import BaseModel

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


class Answer(BaseModel):
    given: str
    expected: str
    correct: bool


class TrainView(View):
    @staticmethod
    def _retrieve_from_session(request, key: str) -> str | None:
        if key in request.session:
            return request.session.pop(key)

    def get(self, request, *args, **kwargs):
        vokabel = models.Vokabel.objects.order_by("?").first()
        if "answer" in request.session:
            answer = Answer(**self.request.session.pop("answer"))
        else:
            answer = None

        context = {
            "vokabel": vokabel,
            "answer": answer,
        }
        return render(request, "trainer/train.html", context)

    def post(self, request, **kwargs):
        form = request.POST.dict()
        answer = form.get("answer")
        vokabel_id = form.get("vokabel_id")
        vokabel = models.Vokabel.objects.get(id=vokabel_id)

        request.session["answer"] = Answer(
            given=vokabel.deutsch,
            expected=vokabel.englisch,
            correct=answer == vokabel.englisch,
        ).model_dump(mode="json")

        return HttpResponseRedirect(request.path_info)


def start(request):
    return render(request, "trainer/index.html")
