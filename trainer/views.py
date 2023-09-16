from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, SingleTableView
from pydantic import BaseModel

from trainer import models, tables, filters, forms


class VokabelGroupView(SingleTableView):
    model = models.VokabelGroup
    template_name = "trainer/vokabelgroup.html"
    table_class = tables.VokabelGroupTable


class AddVokabelGroupView(CreateView):
    model = models.VokabelGroup
    fields = ["name"]
    template_name_suffix = "_create_form"
    success_url = reverse_lazy("trainer:group_list")


class UpdateVokabelGroupView(UpdateView):
    model = models.VokabelGroup
    fields = ["name"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("trainer:group_list")


class DeleteVokabelGroupView(DeleteView):
    model = models.VokabelGroup
    template_name_suffix = "_delete_form"
    success_url = reverse_lazy("trainer:group_list")


class VokabelView(SingleTableMixin, FilterView):
    model = models.Vokabel
    template_name = "trainer/vokabel.html"
    table_class = tables.VokabelTable
    filterset_class = filters.VokabelTableFilter


class AddVokabelView(CreateView):
    form_class = forms.CreateVokabelForm
    template_name = "trainer/vokabel_create_form.html"
    success_url = reverse_lazy("trainer:add")


class UpdateVokabelView(UpdateView):
    model = models.Vokabel
    fields = ["deutsch", "englisch", "group"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("trainer:list")


# TODO add vokabel details to delete template
class DeleteVokabelView(DeleteView):
    model = models.Vokabel
    template_name_suffix = "_delete_form"
    success_url = reverse_lazy("trainer:list")


# TODO move to ???
class Answer(BaseModel):
    asked: str
    expected: str
    actual: str
    correct: bool


# TODO move to ???
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
    def _load_train_session(self) -> TrainSession:
        if "train_session" in self.request.session:
            return TrainSession(**self.request.session.get("train_session"))
        else:
            return TrainSession()

    def _save_train_session(self, train_session: TrainSession) -> None:
        self.request.session["train_session"] = train_session.model_dump(mode="json")

    def get(self, request, *args, **kwargs):
        vokabel = models.Vokabel.objects.order_by("?").first()
        train_session = self._load_train_session()

        context = {
            "form": forms.TrainForm(
                initial={"deutsch": vokabel.deutsch, "id": vokabel.id}
            ),
            "vokabel": vokabel,
            "answer": train_session.last_answer,
            "train_session": train_session,
        }
        train_session.last_answer = None
        self._save_train_session(train_session)
        return render(request, "trainer/train.html", context)

    def post(self, request, **kwargs):
        if "reset" in request.POST:
            request.session["train_session"] = TrainSession().model_dump(mode="json")
            return HttpResponseRedirect(request.path_info)

        train_session = self._load_train_session()

        form = forms.TrainForm(request.POST)
        answer = form.data["englisch"]
        vokabel_id = form.data["id"]
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
        self._save_train_session(train_session)

        return HttpResponseRedirect(request.path_info)


def start(request):
    return render(request, "trainer/index.html")
