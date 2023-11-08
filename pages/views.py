from django.shortcuts import render


def home_view(request, *args, **kwargs):
    return render(request, "pages/main.html")


def get_murkelhausen_version(request) -> dict:
    import importlib.metadata

    __version__ = importlib.metadata.version("murkelhausen-app")

    return {"version": __version__}
