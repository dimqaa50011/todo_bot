from .adding_notify import register_adding_notify_handlers
from .adding_tasks import register_adding_tasks_handlers
from .admin import register_admin_hanlers
from .echo import register_echo_handler
from .set_timezone import register_set_timezone_handlers
from .start import register_start_handlers
from .tasks_list import register_tasks_list_handlers

__all__ = [
    "register_start_handlers",
    "register_echo_handler",
    "register_admin_hanlers",
    "register_adding_tasks_handlers",
    "register_adding_notify_handlers",
    "register_set_timezone_handlers",
    "register_tasks_list_handlers",
]
