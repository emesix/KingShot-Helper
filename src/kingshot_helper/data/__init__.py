import json
from functools import lru_cache
from importlib.resources import files
from typing import Any


def _data_dir():
    return files("kingshot_helper") / "data"


@lru_cache
def load_json(filename: str) -> Any:
    ref = _data_dir() / filename
    return json.loads(ref.read_text(encoding="utf-8"))
