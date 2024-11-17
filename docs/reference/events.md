---
title: Events
---

::: pydantic_gitlab_webhooks.events
    options:
      heading_level: 1
      show_root_heading: true
      show_root_full_path: true

## Generic models

The `AnyEvent` model represents any event body which may be present in a GitHub webhook.

::: pydantic_gitlab_webhooks.events
    options:
      show_if_no_docstring: true
      show_bases: false
      show_labels: false
      filters:
        - "^AnyEvent"

## Event-specific models

Specific types of event each have their own Pydantic model.

::: pydantic_gitlab_webhooks.events
    options:
      show_if_no_docstring: true
      show_bases: false
      show_labels: false
      inherited_members: true
      filters:
        - "!^_"
        - "!^Any"
