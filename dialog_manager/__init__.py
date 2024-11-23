from typing import Callable
from .status import DialogStatus
from .request import DialogRequest
from .response import DialogResponse

StatusHandler = Callable[[DialogRequest, DialogResponse], dict]  # Custom type for annotations

CALLBACKS: dict[DialogStatus, StatusHandler] = {}

# The aim here is to 'register' given function as a callback for a certain dialog status
# as well as make it provide flask-friendly json output automatically
def status_handler(status_id: DialogStatus) -> Callable:
    def inner(func: StatusHandler) -> StatusHandler:
        def wrapper(req: DialogRequest, res: DialogResponse) -> dict:
            func(req, res)  # Decorated functions must take Request and Response as their arguments
            return res.json

        CALLBACKS[status_id] = wrapper
        return wrapper

    return inner

def get_callback(status: DialogStatus) -> StatusHandler:
    return CALLBACKS[status]
