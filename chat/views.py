from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView
from pydantic import BaseModel

from chat import forms, models, tables
from chat.openai.main import generate_chat_completion


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
        print(f"last_question: {last_question}")
        self.request.session["last_qa_question"] = last_question.model_dump(mode="json")

    def _load_last_qa_question(self) -> LastQAQuestion | None:
        try:
            answer = self.LastQAQuestion(**self.request.session.get("last_qa_question"))
        except TypeError:
            answer = None
        print(f"answer: {answer}")
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
            answer, error_msg = generate_chat_completion(input_message)
            self._save_last_qa_question(
                input_message=input_message, answer=answer, error_msg=error_msg
            )

        return HttpResponseRedirect(request.path_info)


class ChatSystemView(SingleTableView):
    model = models.ChatSystem
    template_name = "chat/chatsystem.html"
    table_class = tables.ChatSystemTable


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
