from django.shortcuts import render


def home_view(request, *args, **kwargs):
    import importlib.metadata

    __version__ = importlib.metadata.version("murkelhausen-app")
    return render(request, "pages/main.html", {"version": __version__})
