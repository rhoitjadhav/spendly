import json
from datetime import date, datetime


def to_dict(obj: str) -> dict:
    return json.loads(obj)


def convert_to_date(date_str: str, fmt: str = "%d-%m-%Y") -> date:
    return datetime.strptime(date_str, fmt).date()
