from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views import generic, View
from pydantic import BaseModel

from trainer import models


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
    asked: str
    expected: str
    actual: str
    correct: bool


class TrainSession(BaseModel):
    correct: int = 0
    wrong: int = 0
    last_answer: Answer | None = None

    @property
    def total(self):
        return self.correct + self.wrong

    @property
    def correct_percentage(self):
        try:
            return self.correct / self.total * 100
        except ZeroDivisionError:
            return 0


class TrainView(View):
    def _get_train_session(self) -> TrainSession:
        if "train_session" in self.request.session:
            return TrainSession(**self.request.session.get("train_session"))
        else:
            return TrainSession()

    def _set_train_session(self, train_session: TrainSession) -> None:
        self.request.session["train_session"] = train_session.model_dump(mode="json")

    def get(self, request, *args, **kwargs):
        vokabel = models.Vokabel.objects.order_by("?").first()
        train_session = self._get_train_session()

        context = {
            "vokabel": vokabel,
            "answer": train_session.last_answer,
            "train_session": train_session,
        }
        train_session.last_answer = None
        self._set_train_session(train_session)
        return render(request, "trainer/train.html", context)

    def post(self, request, **kwargs):
        print(request.POST)
        if "reset" in request.POST:
            request.session["train_session"] = TrainSession().model_dump(mode="json")
            return HttpResponseRedirect(request.path_info)

        train_session = self._get_train_session()

        form = request.POST.dict()
        answer = form.get("answer")
        vokabel_id = form.get("vokabel_id")
        vokabel = models.Vokabel.objects.get(id=vokabel_id)
        correct = answer == vokabel.englisch
        if correct:
            train_session.correct += 1
        else:
            train_session.wrong += 1

        train_session.last_answer = Answer(
            asked=vokabel.deutsch,
            expected=vokabel.englisch,
            actual=answer,
            correct=correct,
        )
        self._set_train_session(train_session)

        return HttpResponseRedirect(request.path_info)


def start(request):
    return render(request, "trainer/index.html")
