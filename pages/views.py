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
        base_url1 = "http://rasp1.local/admin/api.php"
        base_url2 = "http://rasp2.local/admin/api.php"
        token = settings.PI_HOLE_TOKEN
        params = {
            "auth": token,
            "disable": 300,
        }
        try:
            r1 = requests.get(base_url1, params=params)
        except requests.exceptions.ConnectionError:
            logger.error("Connection to rasp1 failed.")
            r1 = None
        else:
            logger.info(f"Response from rasp1: {r1.text}; {r1.status_code}.")
        try:
            r2 = requests.get(base_url2, params=params)
        except requests.exceptions.ConnectionError:
            logger.error("Connection to rasp2 failed.")
            r2 = None
        else:
            logger.info(f"Response from rasp2: {r2.text}; {r2.status_code}.")

        if r1 and r1.status_code == 200 and r2 and r2.status_code == 200:
            logger.info("Successfully disabled PI-Hole.")
            messages.success(request, "Pi Hole has been deactivated for 5 minutes.")
        else:
            logger.error("Failed to disable PI-Hole.")
            messages.error(
                request,
                f"Failed to deactivate Pi Hole. Contact Arkadius. ;)\n"
                f"{r1.text=}; r1.status_code={r1.status_code=} \n"
                f"{r2.text=}; r2.status_code={r2.status_code=}",
            )

        return HttpResponseRedirect(reverse("home"))


def get_murkelhausen_version(request) -> dict:
    import importlib.metadata

    __version__ = importlib.metadata.version("murkelhausen-app")

    return {"version": __version__}
