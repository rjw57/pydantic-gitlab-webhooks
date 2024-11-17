import pytest

from pydantic_gitlab_webhooks import (
    validate_event_body_dict,
    validate_event_header_and_body_dict,
)
from pydantic_gitlab_webhooks.events import (
    CommitNoteEvent,
    DeploymentEvent,
    EmojiEvent,
    FeatureFlagEvent,
    GroupAccessTokenEvent,
    GroupMemberEvent,
    IssueEvent,
    IssueNoteEvent,
    JobEvent,
    MergeRequestEvent,
    MergeRequestNoteEvent,
    PipelineEvent,
    ProjectAccessTokenEvent,
    ProjectEvent,
    PushEvent,
    ReleaseEvent,
    SnippetNoteEvent,
    SubgroupEvent,
    TagPushEvent,
    WikiPageEvent,
)

from .conftest import ALL_EVENT_FIXTURE_NAMES, HEADER_AND_FIXTURE_NAMES

FIXTURE_NAMES_AND_EXPECTED_TYPES = {
    "commit-comment": CommitNoteEvent,
    "deployment": DeploymentEvent,
    "emoji": EmojiEvent,
    "feature-flag": FeatureFlagEvent,
    "group-access-request": GroupMemberEvent,
    "group-access-request-denied": GroupMemberEvent,
    "group-access-token": GroupAccessTokenEvent,
    "group-add-member": GroupMemberEvent,
    "group-remove-member": GroupMemberEvent,
    "group-update-member": GroupMemberEvent,
    "issue": IssueEvent,
    "issue-comment": IssueNoteEvent,
    "job": JobEvent,
    "mr": MergeRequestEvent,
    "mr-comment": MergeRequestNoteEvent,
    "pipeline": PipelineEvent,
    "project-access-token": ProjectAccessTokenEvent,
    "project-create": ProjectEvent,
    "project-delete": ProjectEvent,
    "push": PushEvent,
    "release": ReleaseEvent,
    "snippet-comment": SnippetNoteEvent,
    "subgroup-create": SubgroupEvent,
    "subgroup-remove": SubgroupEvent,
    "tag": TagPushEvent,
    "wiki": WikiPageEvent,
}


@pytest.mark.parametrize("event_body", ALL_EVENT_FIXTURE_NAMES, indirect=True)
def test_event_parses(event_body):
    "Event test fixture parses"
    validate_event_body_dict(event_body)


@pytest.mark.parametrize(
    "event_body,expected_type",
    FIXTURE_NAMES_AND_EXPECTED_TYPES.items(),
    indirect=["event_body"],
)
def test_inferred_event_type(event_body, expected_type):
    "Event types are correctly inferred from event body"
    assert isinstance(validate_event_body_dict(event_body), expected_type)


@pytest.mark.parametrize("header,event_body", HEADER_AND_FIXTURE_NAMES, indirect=["event_body"])
def test_header_validates(header, event_body):
    "Events parse when associated with incoming request header."
    validate_event_header_and_body_dict(header, event_body)


@pytest.mark.parametrize(
    "header,event_body,expected_type",
    [
        (h, n, FIXTURE_NAMES_AND_EXPECTED_TYPES[n])
        for h, n in HEADER_AND_FIXTURE_NAMES
        if n in FIXTURE_NAMES_AND_EXPECTED_TYPES
    ],
    indirect=["event_body"],
)
def test_header_inferred_type(header, event_body, expected_type):
    "Events types are correctly inferred when parsed with header"
    assert isinstance(validate_event_header_and_body_dict(header, event_body), expected_type)
