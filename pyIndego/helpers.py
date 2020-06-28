"""Helper class for Indego."""
from dataclasses import dataclass
from dataclasses import is_dataclass
from datetime import datetime
import logging
_LOGGER = logging.getLogger(__name__)


def nested_dataclass(*args, **kwargs):  # noqa: D202
    """Wrap a nested dataclass object."""

    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if is_dataclass(field_type) and isinstance(value, dict):
                    new_obj = field_type(**value)
                    kwargs[name] = new_obj
            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper


def convert_bosch_datetime(dt: str = None):
    """Create a datetime object from the string from Bosch. Checks if a valid number of milliseconds is sent."""
    if dt:
        plus_index = dt.find("+")
        dot_index = dt.find(".")
        if dot_index > 0 and plus_index > 0:
            diff = plus_index - dot_index
            if 1 <= diff <= 3:
                dt = dt.replace("+", f"{0*(4-diff)}+")
        return datetime.fromisoformat(dt)
    return None