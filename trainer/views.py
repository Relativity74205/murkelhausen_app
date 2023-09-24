import random

from django.conf import settings
from django.http import HttpResponseRedirect, HttpRequest, QueryDict
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

    def get(self, request: HttpRequest, *args, **kwargs):
        if len(request.GET) == 0:
            last_vokabel_filter = request.session.get("last_vokabel_filter")
            if last_vokabel_filter:
                query_dict = QueryDict("", mutable=True)
                query_dict.update(last_vokabel_filter)
                request.GET = query_dict
        else:
            if "reset" in request.GET:
                request.session["last_vokabel_filter"] = None
                request.GET = QueryDict("")
            else:
                request.session["last_vokabel_filter"] = request.GET
        return super().get(request, *args, **kwargs)


class AddVokabelView(CreateView):
    form_class = forms.CreateVokabelForm
    template_name = "trainer/vokabel_create_form.html"
    success_url = reverse_lazy("trainer:add")

    def get(self, request: HttpRequest, *args, **kwargs):
        group_id = self.request.session.get("last_group_added_to")
        if group_id:
            self.initial["group"] = group_id
        else:
            self.initial["group"] = models.VokabelGroup.objects.order_by(
                "-created"
            ).first()
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        self.request.session["last_group_added_to"] = request.POST["group"]
        return super().post(request, *args, **kwargs)


class UpdateVokabelView(UpdateView):
    model = models.Vokabel
    fields = ["deutsch", "englisch", "group"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("trainer:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trainer_last_n"] = settings.TRAINER_LAST_N
        return context


class DeleteVokabelView(DeleteView):
    model = models.Vokabel
    fields = ["deutsch", "englisch", "group"]
    template_name_suffix = "_delete_form"
    success_url = reverse_lazy("trainer:list")


# TODO move to ???
class Answer(BaseModel):
    asked: str
    expected: str
    actual: str
    correct: bool


# TODO move to ???
# TODO add train session as database model
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

    @staticmethod
    def get_random_vokabel(group_id: int | None) -> models.Vokabel | None:
        # TODO test!
        if group_id is None:
            vokabeln = models.Vokabel.objects.all()
        else:
            vokabeln = models.Vokabel.objects.filter(group__id=group_id).all()

        if len(vokabeln) == 0:
            return None

        weights = [
            (1 - v.correct_percentage_last / 100) * 0.8 + settings.TRAINER_RANDOM_OFFSET
            for v in vokabeln
        ]
        return random.choices(vokabeln, weights=weights)[0]

    def get(self, request: HttpRequest, *args, **kwargs):
        group_id = request.session.get("group_id")
        vokabel = self.get_random_vokabel(group_id)
        train_session = self._load_train_session()

        group_select_form = self._get_group_select_form(group_id)
        if vokabel:
            train_form = forms.TrainForm(
                initial={"deutsch": vokabel.deutsch, "id": vokabel.id}
            )
        else:
            train_form = None

        context = {
            "train_form": train_form,
            "group_select_form": group_select_form,
            "vokabel": vokabel,
            "answer": train_session.last_answer,
            "train_session": train_session,
        }
        train_session.last_answer = None
        self._save_train_session(train_session)
        return render(request, "trainer/train.html", context)

    @staticmethod
    def _get_group_select_form(group_id: int | None):
        group_select_form = forms.VokabelGroupSelectForm()
        group_choices = [(-1, "Alle")]
        group_choices += [
            (group.id, group.name) for group in models.VokabelGroup.objects.all()
        ]
        group_select_form.fields["group"].choices = group_choices
        group_select_form.fields["group"].initial = group_id
        return group_select_form

    def post(self, request: HttpRequest, **kwargs):
        if "reset" in request.POST:
            request.session["train_session"] = TrainSession().model_dump(mode="json")
            return HttpResponseRedirect(request.path_info)
        elif "group" in request.POST:
            group_id = request.POST["group"]
            if group_id == "-1":
                self.request.session["group_id"] = None
            else:
                self.request.session["group_id"] = group_id

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
        vokabel.results.append(correct)
        vokabel.save()

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
