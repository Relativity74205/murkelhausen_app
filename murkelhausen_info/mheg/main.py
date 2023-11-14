import time
from datetime import date
from functools import lru_cache

import requests
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel
from babel.dates import format_date

BASE_URL = "https://muelheim-abfallapp.regioit.de/abfall-app-muelheim/rest/"


class Bezirk(BaseModel):
    id: int
    name: str
    gueltigAb: str | None
    fraktionId: int


class MuellTermine(BaseModel):
    id: int
    bezirk: Bezirk
    datum: date

    @property
    def art(self) -> str:
        match self.bezirk.fraktionId:
            case 0:
                return "Restmüll"
            case 1:
                return "Papier"
            case 2:
                return "Gelbe Tonne"
            case 3:
                return "Biotonne"
            case _:
                return "Unbekannt"

    @property
    def delta_days(self) -> int:
        return (self.datum - date.today()).days

    @property
    def day(self) -> str:
        return format_date(self.datum, format="EEE, d.M.yyyy", locale="de_DE")


@lru_cache(maxsize=1)
def get_orte(_: int) -> list[dict]:
    """
    Request url: https://muelheim-abfallapp.regioit.de/abfall-app-muelheim/rest/orte
    Example response: [{"id":4103948,"name":"Mülheim"}]
    """
    # TODO add error handling
    url = BASE_URL + "orte"
    r = requests.get(url)
    orte = r.json()

    return orte


def get_muelheim_id() -> int:
    ttl_seconds = 60 * 60 * 24 * 7  # 7 days
    orte = get_orte(round(time.time() / ttl_seconds))
    muelheim_id = next((ort["id"] for ort in orte if ort["name"] == "Mülheim"), None)

    return muelheim_id


@lru_cache(maxsize=1)
def get_strassen(muelheim_id: int, _: int) -> list[dict]:
    """
    Example request url: "https://muelheim-abfallapp.regioit.de/abfall-app-muelheim/rest/orte/4103948/strassen"
    Example response:
    [{
        "id": 4134672,
        "name": "Zunftmeisterstraße",
        "staticId": "TfxsaGVpbWRlZmF1bHRadW5mdG1laXN0ZXJzdHJh32U=",
        "hausNrList": [],
        "plz": null,
        "ortsteilName": "default",
        "ort": {
          "id": 4103948,
          "name": "Mülheim"
        }
    },
    {
        "id": 4134679,
        "name": "Zur Alten Dreherei",
        "staticId": "TfxsaGVpbWRlZmF1bHRadXIgQWx0ZW4gRHJlaGVyZWk=",
        "hausNrList": [],
        "plz": null,
        "ortsteilName": "default",
        "ort": {
          "id": 4103948,
          "name": "Mülheim"
        }
      },
    ...]
    """

    # TODO add error handling
    url = BASE_URL + f"orte/{muelheim_id}/strassen"
    r = requests.get(url)
    strassen = r.json()

    return strassen


def get_friedhofstrassen_id() -> int:
    target_street = "Friedhofstraße"
    ttl_seconds = 60 * 60 * 24 * 7  # 7 days
    muelheim_id = get_muelheim_id()
    strassen = get_strassen(muelheim_id, round(time.time() / ttl_seconds))
    friedhofstrassen_id = next(
        (strasse["id"] for strasse in strassen if strasse["name"] == target_street),
        None,
    )

    return friedhofstrassen_id


@lru_cache(maxsize=1)
def get_hausnummern(strassen_id: int, _: int) -> list[dict]:
    """
    Example request url: "https://muelheim-abfallapp.regioit.de/abfall-app-muelheim/rest/strassen/4112491"
    Example response:
    {
        "id": 4112491,
        "name": "Friedhofstraße",
        "staticId": "TfxsaGVpbWRlZmF1bHRGcmllZGhvZnN0cmHfZQ==",
        "hausNrList": [
            {
                "id": 4112629,
                "nr": "9",
                "plz": "45478",
                "staticId": "TfxsaGVpbTQ1NDc4RnJpZWRob2ZzdHJh32U5"
            },
            ...
            {
                "id": 4112579,
                "nr": "212",
                "plz": "45478",
                "staticId": "TfxsaGVpbTQ1NDc4RnJpZWRob2ZzdHJh32UyMTI="
            }
        ],
        "plz": null,
        "ortsteilName": "default",
        "ort": {
          "id": 4103948,
          "name": "Mülheim"
        }
    }
    """
    # TODO add error handling
    url = BASE_URL + f"strassen/{strassen_id}"
    r = requests.get(url)
    strassen = r.json()

    return strassen


def get_friedhofstrassen_62_id() -> int:
    target_hausnummer = 62
    strassen_id = get_friedhofstrassen_id()
    ttl_seconds = 60 * 60 * 24 * 7  # 7 days
    hausnummern = get_hausnummern(strassen_id, round(time.time() / ttl_seconds))
    friedhofstrassen_62_id = next(
        (
            hausnummer["id"]
            for hausnummer in hausnummern["hausNrList"]
            if hausnummer["nr"] == str(target_hausnummer)
        ),
        None,
    )

    return friedhofstrassen_62_id


@lru_cache(maxsize=1)
def get_termine(hausnummer_id: int, _: int) -> list[dict]:
    """
    Example request url: "https://muelheim-abfallapp.regioit.de/abfall-app-muelheim/rest/hausnummern/4112605/termine"
    Example response:
    [{
        "id": 4134780,
        "bezirk": {
            "id": 4103952,
            "name": "R2",
            "gueltigAb": null,
            "fraktionId": 0
        },
        "datum": "2023-01-05"
    },
    ...
    ]
    """
    url = BASE_URL + f"hausnummern/{hausnummer_id}/termine"
    r = requests.get(url)
    termine = r.json()

    return termine


def get_termine_for_home() -> list[MuellTermine]:
    hausnummer_id = get_friedhofstrassen_62_id()

    ttl_seconds = 60 * 60 * 24  # 1 day
    termine_dict = get_termine(hausnummer_id, round(time.time() / ttl_seconds))
    termine = [MuellTermine(**termin) for termin in termine_dict]
    termine = filter_termine(termine)
    termine = sorted(termine, key=lambda termin: termin.datum)

    return termine


def filter_termine(
    termine: list[MuellTermine], month_limit: int = 2
) -> list[MuellTermine]:
    """Returns termine after today and within the next month_limit months."""
    return [
        termin
        for termin in termine
        if date.today()
        <= termin.datum
        <= date.today() + relativedelta(months=month_limit)
    ]
