import datetime
from typing import Annotated

import dateutil.parser
from pydantic import AwareDatetime
from pydantic.functional_validators import BeforeValidator


def _parse_datetime(v: str):
    try:
        return dateutil.parser.parse(v)
    except (dateutil.parser.ParserError, OverflowError) as e:
        raise ValueError(f"Failed to parse timestamp: {e}")


def _parse_date(v: str):
    try:
        return dateutil.parser.parse(v).date()
    except (dateutil.parser.ParserError, OverflowError) as e:
        raise ValueError(f"Failed to parse date: {e}")


Datetime = Annotated[AwareDatetime, BeforeValidator(_parse_datetime)]
Date = Annotated[datetime.date, BeforeValidator(_parse_date)]
