# Pydantic models for GitLab Webhooks

Module containing Pydantic models for validating bodies from [GitLab webhook
requests](https://docs.gitlab.com/ee/user/project/integrations/webhook_events.html).

## Usage

Intended usage is via a single `validate_event_header_and_body` function which will validate an
incoming webhook's `X-Gitlab-Event` header and the body after being parsed into a Python dict.

```py
from pydantic import ValidationError
from pydantic_gitlab_webhooks import validate_event_header_and_body, validate_event_dict

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

# Use the value of the "X-Gitlab-Event" header and event body to validate the incoming event.
parsed_event = validate_event_header_and_body(
    "Resource Access Token Hook",
    event_body
)
assert parsed_event.group.full_path == "twitter"

# Invalid event bodies or hook headers raise Pydantic validation errors
try:
    validate_event_header_and_body("invalid hook", event_body)
except ValidationError:
    pass  # ok - expected error raised
else:
    assert False, "ValidationError was not raised"

# Event bodies can be parsed without the header hook if necessary although using the hook header is
# more efficient.
parsed_event = validate_event_dict(event_body)
assert parsed_event.group.full_path == "twitter"
```
