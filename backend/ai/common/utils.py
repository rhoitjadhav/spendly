import json


def to_dict(obj: str) -> dict:
    return json.loads(obj)
