from murkelhausen_info.models import MurkelhausenStates, PowerData

ROUTED_MODELS = [MurkelhausenStates, PowerData]


class MurkelhausenInfoRouter:
    def db_for_read(self, model, **hints):
        if model in ROUTED_MODELS:
            return "data"
        return None

    def db_for_write(self, model, **hints):
        if model in ROUTED_MODELS:
            return "data"
        return None
