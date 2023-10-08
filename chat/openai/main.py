from enum import StrEnum, auto

import openai


image_resp = openai.Image.create(
    prompt="two dogs playing chess, oil painting", n=4, size="512x512"
)


class OpenAIModel(StrEnum):
    GPT35TURBO = "gpt-3.5-turbo"
    GPT4 = "gpt-4"


def generate_chat_completion(
    input_message: str, model: OpenAIModel = OpenAIModel.GPT35TURBO
) -> str:
    """
    https://platform.openai.com/docs/guides/gpt/chat-completions-api
    https://platform.openai.com/docs/api-reference/chat/create

    TODOs
    - [ ] count usage tokens from answer
    - [ ] evaluate finish_reason
    """
    completion = openai.ChatCompletion.create(
        model=model, messages=[{"role": "user", "content": input_message}]
    )

    answer = completion.choices[0].message.content

    return answer


def speech_to_text():
    """https://github.com/openai/openai-python#audio-whisper"""
    raise NotImplementedError


def generate_image():
    """https://github.com/openai/openai-python#image-generation-dalle"""
    raise NotImplementedError
