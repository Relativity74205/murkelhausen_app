import logging

import requests
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from murkelhausen_app import settings

logger = logging.getLogger(__name__)


def home_view(request, *args, **kwargs):
    return render(request, "pages/main.html")


def pihole_deactivate(request, *args, **kwargs):
    if request.method == "POST":
        logger.info("Disabling PI-Hole for 5 minutes.")
        base_url1 = "http://192.168.1.18/admin/api.php"  # rasp1.local
        base_url2 = "http://192.168.1.28/admin/api.php"  # rasp2.local

        _deactivate_pihole(request, base_url1, 1)
        _deactivate_pihole(request, base_url2, 2)

        return HttpResponseRedirect(reverse("home"))


def _deactivate_pihole(request, base_url: str, pi_hole_number: int) -> str:
    token = settings.PI_HOLE_TOKEN
    params = {
        "auth": token,
        "disable": 300,
    }
    try:
        r1 = requests.get(base_url, params=params)
    except requests.exceptions.ConnectionError:
        logger.error("Connection to rasp1 failed.")
        messages.error(
            request,
            f"Failed to deactivate Pi Hole {pi_hole_number} due to a connection error. Contact Arkadius. ;)",
        )
    else:
        logger.info(f"Response from rasp{pi_hole_number}: {r1.text}; {r1.status_code}.")
        if r1.status_code == 200:
            messages.success(
                request, f"Pi Hole {pi_hole_number} has been deactivated for 5 minutes."
            )
        else:
            messages.error(
                request,
                f"Failed to deactivate Pi Hole {pi_hole_number}. Contact Arkadius. ;)\n"
                f"{r1.text=}; r1.status_code={r1.status_code=}",
            )


def get_murkelhausen_version(request) -> dict:
    import importlib.metadata

    __version__ = importlib.metadata.version("murkelhausen-app")

    return {"version": __version__}
