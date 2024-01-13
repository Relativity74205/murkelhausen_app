from datetime import date, datetime
from typing import Annotated
import logging

import requests
from cachetools import TTLCache, cached
from pydantic import BaseModel, BeforeValidator, field_validator

logger = logging.getLogger(__name__)


def replace_empty_str_with_none(v: str) -> str | None:
    if v == "":
        return None
    return v


VertretungsplanString = Annotated[
    str | None, BeforeValidator(replace_empty_str_with_none)
]


class VertretungsplanEventText(BaseModel):
    text: str
    cancelled: bool


class VertretungsplanEvent(BaseModel):
    classes: tuple[str, ...]
    lessons: tuple[int, ...]
    previousSubject: VertretungsplanString
    subject: VertretungsplanString
    previousRoom: VertretungsplanString
    room: VertretungsplanString
    previousTeacher: VertretungsplanString
    teacher: VertretungsplanString
    texts: VertretungsplanEventText

    @field_validator("texts", mode="before")
    @classmethod
    def convert_texts(cls, v: tuple[str, str]) -> VertretungsplanEventText:
        return VertretungsplanEventText(
            text=v[0], cancelled=True if v[1] == "x" else False
        )

    class Config:
        str_strip_whitespace = True  # remove trailing whitespace


class Vertretungsplan(BaseModel):
    date: date
    version: datetime
    infos: tuple[str, ...]
    events: tuple[VertretungsplanEvent, ...]


@cached(cache=TTLCache(maxsize=1, ttl=60))
def get_vertretungsplan_dates() -> tuple[date, ...]:
    url = "https://assets.gymnasium-broich.de/vplan/api/dates"
    data = requests.get(url).json()
    logger.info(
        f"Retrieved {len(data)} dates of the Vertretungsplan API for which Vertretungsplaene exist."
    )

    return tuple(date.fromisoformat(d) for d in data)


@cached(cache=TTLCache(maxsize=1, ttl=60))
def get_vertretungsplan(datum: date) -> Vertretungsplan:
    base_url = "https://assets.gymnasium-broich.de/vplan/api/"
    data: dict = requests.get(base_url + datum.isoformat()).json()
    logger.info(f"Retrieved Vertretungsplan for {datum}.")

    return Vertretungsplan(**data)
