"""Helper class for Indego."""
import logging
from dataclasses import dataclass, is_dataclass
from datetime import datetime
from typing import Any

_LOGGER = logging.getLogger(__name__)


def nested_dataclass(*args, **kwargs):  # noqa: D202
    """Wrap a nested dataclass object."""

    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                field_type = cls.__annotations__.get(name, None)
                if hasattr(field_type, "__args__"):
                    inner_type = field_type.__args__[0]
                    if is_dataclass(inner_type):
                        new_obj = [inner_type(**dict_) for dict_ in value]
                        kwargs[name] = new_obj
                else:
                    if is_dataclass(field_type) and isinstance(value, dict):
                        new_obj = field_type(**value)
                        kwargs[name] = new_obj

            original_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper


def convert_bosch_datetime(dt: Any = None) -> datetime:
    """Create a datetime object from the string (or give back the datetime object) from Bosch. Checks if a valid number of milliseconds is sent."""
    if dt:
        if isinstance(dt, str):
            if dt.find(".") > 0:
                return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f%z")
            return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S%z")
        if isinstance(dt, datetime):
            return dt
    return None
