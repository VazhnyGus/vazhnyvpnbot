from outline_api import Manager
from typing import Optional, Tuple

from config import config


API_URL = config("OUTLINE_API_URL")
API_CERT = config("OUTLINE_API_CERT")


manager = Manager(apiurl=API_URL, apicrt=API_CERT)


def get_key_from_api() -> Tuple[Optional[str], Optional[int]]:
    key = manager.new()
    if key:
        return key.get("accessUrl"), int(key.get("id"))
    else:
        return None, None


def delete_key_from_api(key_id: int) -> bool:
    return manager.delete(key_id)


def get_usage(key_id: int) -> int:
    return manager.usage(key_id)
