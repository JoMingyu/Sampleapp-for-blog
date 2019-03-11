from abc import abstractmethod
from enum import Enum
from functools import wraps
from typing import Type

from flask import request
from schematics import Model

from app.context import context_property


class PayloadLocation(Enum):
    ARGS = 'args'
    JSON = 'json'


class BaseModel(Model):
    @abstractmethod
    def validate_additional(self):
        pass


def validate_with_schematics(validation_target: PayloadLocation, model: Type[BaseModel]):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            instance = model(getattr(request, validation_target.value))
            instance.validate()
            getattr(instance, 'validate_additional', lambda: ...)()

            context_property.request_payload_object = instance

            return fn(*args, **kwargs)
        return wrapper
    return decorator
