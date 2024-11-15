import json
import os

import pytest

HEADER_AND_FIXTURE_NAMES = [
    ("Deployment Hook", "deployment"),
    ("Emoji Hook", "emoji"),
    ("Feature Flag Hook", "feature-flag"),
    ("Issue Hook", "issue"),
    ("Job Hook", "job"),
    ("Member Hook", "group-access-request"),
    ("Member Hook", "group-access-request-denied"),
    ("Member Hook", "group-add-member"),
    ("Member Hook", "group-remove-member"),
    ("Member Hook", "group-update-member"),
    ("Merge Request Hook", "mr"),
    ("Note Hook", "commit-comment"),
    ("Note Hook", "issue-comment"),
    ("Note Hook", "mr-comment"),
    ("Note Hook", "snippet-comment"),
    ("Pipeline Hook", "pipeline"),
    ("Project Hook", "project-create"),
    ("Project Hook", "project-delete"),
    ("Push Hook", "push"),
    ("Release Hook", "release"),
    ("Resource Access Token Hook", "group-access-token"),
    ("Resource Access Token Hook", "project-access-token"),
    ("Subgroup Hook", "subgroup-create"),
    ("Subgroup Hook", "subgroup-remove"),
    ("Tag Push Hook", "tag"),
    ("Wiki Page Hook", "wiki"),
]

ALL_EVENT_FIXTURE_NAMES = [name for _, name in HEADER_AND_FIXTURE_NAMES]

ALL_EVENT_TYPES = list({event for event, _ in HEADER_AND_FIXTURE_NAMES})

FIXTURE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "fixtures"))


@pytest.fixture
def event_body(request):
    with open(os.path.join(FIXTURE_DIR, f"{request.param}.json")) as f:
        return json.load(f)
