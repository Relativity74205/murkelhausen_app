from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from chat import forms
from chat.openai.main import generate_chat_completion


def start(request):
    return render(request, "chat/index.html")


class QAView(View):
    def _save_chat(self, output: str):
        self.request.session["qa_answer"] = output

    def _load_chat(self) -> str:
        return self.request.session.get("qa_answer", "")

    def get(self, request, *args, **kwargs):
        context = {
            "qa_form": forms.QAForm(),
            "qa_answer": self._load_chat(),
        }
        return render(request, "chat/qa.html", context=context)

    def post(self, request, *args, **kwargs):
        chat_form = forms.QAForm(request.POST)
        if chat_form.is_valid():
            input_message = chat_form.cleaned_data["input"]
            # TODO: Add some kind of error handling, especially if no API key is set
            answer = generate_chat_completion(input_message)
            self._save_chat(answer)

        return HttpResponseRedirect(request.path_info)
