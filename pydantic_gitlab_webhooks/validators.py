from pydantic import TypeAdapter

from .events import AnyEvent, _AnyParseableEvent
from .hooks import _AnyHook

__all__ = [
    "validate_event_body_dict",
    "validate_event_header_and_body_dict",
]


_EVENT_VALIDATOR = TypeAdapter(_AnyParseableEvent)
_HOOK_VALIDATOR = TypeAdapter(_AnyHook)


def validate_event_body_dict(event: dict) -> AnyEvent:
    """
    Validate an incoming event body against the incoming webhook schema.

    Args:
        event: Python dictionary representing the received event body

    Returns:
        a validated and parsed event
    """
    return _EVENT_VALIDATOR.validate_python(event)


def validate_event_header_and_body_dict(header: str, body: dict) -> AnyEvent:
    """
    Validate an event header body against the webhook schema.

    Args:
        header: Value of the X-Gitlab-Event header
        body: Python dictionary representing the received event body

    Returns:
        a validated and parsed event
    """
    return _HOOK_VALIDATOR.validate_python({"header": header, "event_body": body}).event_body
