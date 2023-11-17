import json

from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from pydantic import BaseModel

from chat import forms, models, tables, filters
from chat.openai.main import generate_chat_completion, generate_chat_completion_stream


def start(request):
    return render(request, "chat/index.html")


class QAView(View):
    class LastQAQuestion(BaseModel):
        question: str
        answer: str | None
        error_msg: str | None

    def _save_last_qa_question(
        self, *, input_message: str, answer: str | None, error_msg: str | None
    ):
        last_question = self.LastQAQuestion(
            question=input_message, answer=answer, error_msg=error_msg
        )
        self.request.session["last_qa_question"] = last_question.model_dump(mode="json")

    def _load_last_qa_question(self) -> LastQAQuestion | None:
        try:
            answer = self.LastQAQuestion(**self.request.session.get("last_qa_question"))
        except TypeError:
            answer = None
        self.request.session["last_qa_question"] = None
        return answer

    def get(self, request, *args, **kwargs):
        context = {
            "qa_form": forms.QAForm(),
            "last_qa_question": self._load_last_qa_question(),
        }
        return render(request, "chat/qa.html", context=context)

    def post(self, request, *args, **kwargs):
        chat_form = forms.QAForm(request.POST)
        if chat_form.is_valid():
            input_message = chat_form.cleaned_data["input"]
            system_name = chat_form.cleaned_data["system"]
            try:
                system = models.ChatSystem.objects.get(name=system_name)
                system_setup_text = system.system_setup_text
            except (models.ChatSystem.DoesNotExist, AttributeError):
                system_setup_text = None

            answer, error_msg = generate_chat_completion(
                input_message=input_message, system_setup_text=system_setup_text
            )

            self._save_last_qa_question(
                input_message=input_message, answer=answer, error_msg=error_msg
            )

        return HttpResponseRedirect(request.path_info)


class ChatSystemView(SingleTableMixin, FilterView):
    model = models.ChatSystem
    template_name = "chat/chatsystem.html"
    table_class = tables.ChatSystemTable
    filterset_class = filters.ChatSystemFilter


class AddChatSystemView(CreateView):
    model = models.ChatSystem
    fields = ["name", "system_setup_text"]
    template_name_suffix = "_create_form"
    success_url = reverse_lazy("chat:chatsystem_list")


class UpdateChatSystemView(UpdateView):
    model = models.ChatSystem
    fields = ["name", "system_setup_text"]
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("chat:chatsystem_list")


class DeleteChatSystemView(DeleteView):
    model = models.ChatSystem
    template_name_suffix = "_delete_form"
    success_url = reverse_lazy("chat:chatsystem_list")


def call_openai_api(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    if not is_ajax or request.method != "POST":
        return HttpResponseBadRequest("Invalid request")

    data = json.load(request)
    input_message = data.get("input", None)
    system_id = data.get("system", None)
    try:
        system = models.ChatSystem.objects.get(id=system_id)
        system_setup_text = system.system_setup_text
    except (models.ChatSystem.DoesNotExist, AttributeError, ValueError):
        system_setup_text = None

    answer, finished = get_next_delta(input_message, system_setup_text)

    response = {
        "answer": answer,
        "request_finished": finished,
    }

    return JsonResponse(response)


def get_next_delta(
    input_message: str, system_setup_text: str, count_tokens: int = 5
) -> tuple[str, bool]:
    answer = ""
    for _ in range(count_tokens):
        single_token, finished = generate_chat_completion_stream(
            input_message=input_message, system_setup_text=system_setup_text
        )
        if finished:
            return answer, True
        answer += single_token

    return answer, False
