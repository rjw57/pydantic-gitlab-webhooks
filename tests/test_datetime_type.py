import pytest
from dateutil.tz import tzutc
from pydantic import TypeAdapter, ValidationError

from pydantic_gitlab_webhooks._types import Date, Datetime

datetime_adaptor = TypeAdapter(Datetime)
date_adaptor = TypeAdapter(Date)


@pytest.fixture
def datetime(faker):
    "Date time with second-level precision"
    return faker.date_time(tzutc()).replace(microsecond=0)


@pytest.fixture
def date(datetime):
    return datetime.date()


def test_iso_format_timestamp(datetime):
    assert datetime_adaptor.validate_python(datetime.isoformat()) == datetime


def test_gitlab_format_timestamp(datetime):
    assert datetime_adaptor.validate_python(datetime.strftime("%Y-%m-%d %H:%M:%S UTC")) == datetime


def test_timezone_required(datetime):
    with pytest.raises(ValidationError, match="Input should have timezone"):
        datetime_adaptor.validate_python(datetime.strftime("%Y-%m-%d %H:%M:%S"))


def test_bad_timestamp_format():
    with pytest.raises(ValidationError, match="Failed to parse timestamp"):
        datetime_adaptor.validate_python("this is not a timestamp")


def test_iso_format_date(date):
    assert date_adaptor.validate_python(date.isoformat()) == date


def test_bad_date_format():
    with pytest.raises(ValidationError, match="Failed to parse date"):
        date_adaptor.validate_python("this is not a date")
