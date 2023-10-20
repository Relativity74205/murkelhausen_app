import functools
from enum import StrEnum

import openai


class OpenAIModel(StrEnum):
    GPT35TURBO = "gpt-3.5-turbo"
    GPT4 = "gpt-4"


def image_generation():
    raise NotImplementedError
    image_resp = openai.Image.create(
        prompt="two dogs playing chess, oil painting", n=4, size="512x512"
    )


def generate_chat_completion(
    *,
    input_message: str,
    system_setup_text: str | None,
    model: OpenAIModel = OpenAIModel.GPT35TURBO
) -> tuple[str | None, str | None]:
    """
    https://platform.openai.com/docs/guides/gpt/chat-completions-api
    https://platform.openai.com/docs/api-reference/chat/create

    TODOs
    - [ ] count usage tokens from answer
    - [ ] evaluate finish_reason
    """
    messages = []
    if system_setup_text is not None:
        messages.append({"role": "system", "content": system_setup_text})

    messages.append({"role": "user", "content": input_message})

    # TODO count tokes with https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
    try:
        completion = openai.ChatCompletion.create(model=model, messages=messages)
    except openai.error.AuthenticationError:
        return None, "No or wrong API key set"

    answer = completion.choices[0].message.content

    return answer, None


# TODO save stream object in session/ a dict? to handle parallel requests
def save_stream(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not wrapper.results:
            wrapper.results = func(*args, **kwargs)

        delta = next(wrapper.results)

        if delta["choices"][0]["finish_reason"] == "stop":
            wrapper.results = None
            return "", True

        return delta["choices"][0]["delta"]["content"], False

    wrapper.results = None

    return wrapper


@save_stream
def generate_chat_completion_stream(
    *,
    input_message: str,
    system_setup_text: str | None,
    model: OpenAIModel = OpenAIModel.GPT35TURBO
) -> tuple[str, bool]:
    """
    https://platform.openai.com/docs/guides/gpt/chat-completions-api
    https://platform.openai.com/docs/api-reference/chat/create

    TODOs
    - [ ] count usage tokens from answer
    """
    messages = []
    if system_setup_text is not None:
        messages.append({"role": "system", "content": system_setup_text})

    messages.append({"role": "user", "content": input_message})

    delta = openai.ChatCompletion.create(model=model, messages=messages, stream=True)

    return delta


def speech_to_text():
    """https://github.com/openai/openai-python#audio-whisper"""
    raise NotImplementedError


def generate_image():
    """https://github.com/openai/openai-python#image-generation-dalle"""
    raise NotImplementedError
