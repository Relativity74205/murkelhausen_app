import sys
import inspect

from murkelhausen_info.models_old import MurkelhausenStates, PowerData
from murkelhausen_info import models

REPORT_ROUTED_MODELS = [MurkelhausenStates, PowerData]
# DATA_ROUTED_MODELS = [
#     cls_name
#     for cls_name, cls_obj in inspect.getmembers(sys.modules["murkelhausen_info.models"])
#     if inspect.isclass(cls_obj)
# ]
DATA_ROUTED_MODELS = [models.BodyBatteryDaily]


class MurkelhausenInfoRouter:
    def db_for_read(self, model, **hints):
        if model in REPORT_ROUTED_MODELS:
            return "report"
        elif model in DATA_ROUTED_MODELS:
            return "data"
        return None

    def db_for_write(self, model, **hints):
        if model in REPORT_ROUTED_MODELS:
            return "report"
        elif model in DATA_ROUTED_MODELS:
            return "data"
        return None
