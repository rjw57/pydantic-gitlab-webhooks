# Getting started

This page provides a getting started guide for using the package to validate incoming
[GitLab webhook
events](https://docs.gitlab.com/ee/user/project/integrations/webhooks.html).

## Installation

Installation can be done with `pip` from the [PyPI
project](https://pypi.org/p/pydantic-gitlab-webhooks):

```sh
pip install pydantic-gitlab-webhooks
```

## Validating webhook requests

The [pydantic_gitlab_webhooks.validators.validate_event_header_and_body_dict][] function
can be used to validate an incoming GitLab webhook request's headers and body against the
expected schema.

The return value with be [an event model](./reference/events.md) if parsing succeeded
otherwise a `pydantic.ValidationError` will be raised.

For example, to validate and parse the an incoming request in a
[Flask](https://flask.palletsprojects.com/en/stable/) application:

```py
from flask import Flask, request, abort
from pydantic import ValidationError
from pydantic_gitlab_webhooks import validate_event_header_and_body_dict

app = Flask(__name__)

@app.route("/")
def webhook():
    try:
        event = validate_event_header_and_body_dict(
            request.headers["x-gitlab-event"],
            request.json
        )
    except ValidationError:
        abort(400, "Bad Request")

    # ...
```

## Validating specific event types

If you know that a particular event body is expected, you can use the Pydantic models
themselves. For example, if you know that an event should be a Push Event, you can use
the [pydantic_gitlab_webhooks.events.PushEvent][] model:

```py
from flask import Flask, request, abort
from pydantic import ValidationError
from pydantic_gitlab_webhooks.events import PushEvent

app = Flask(__name__)

@app.route("/")
def webhook():
    if request.headers["x-gitlab-event"] != "Push Event":
        abort(400, "Bad event type")
    try:
        event = PushEvent.model_validate(request.json)
    except ValidationError:
        abort(400, "Bad Request")

    # ...
```

## Validating event bodies alone

If you don't have the contents of the `X-Gitlab-Event` header, you can still validate
event bodies but the matching will be slightly less efficient. For example:

```py
from pydantic_gitlab_webhooks import validate_event_body_dict

event_body = {
    "object_kind": "access_token",
    "group": {
        "group_name": "Twitter",
        "group_path": "twitter",
        "group_id": 35,
        "full_path": "twitter"
    },
    "object_attributes": {
        "user_id": 90,
        "created_at": "2024-01-24 16:27:40 UTC",
        "id": 25,
        "name": "acd",
        "expires_at": "2024-01-26"
    },
    "event_name": "expiring_access_token"
}

parsed_event = validate_event_body_dict(event_body)
assert parsed_event.group.full_path == "twitter"
```
