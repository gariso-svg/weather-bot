import json
import logging
import os

logger = logging.getLogger(__name__)

_USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")


def load_chat_ids() -> set[int]:
    try:
        with open(_USERS_FILE, encoding="utf-8") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()
    except (json.JSONDecodeError, ValueError):
        logger.warning("users.json is corrupted; starting with empty user list")
        return set()


def save_chat_id(chat_id: int) -> None:
    ids = load_chat_ids()
    if chat_id in ids:
        return
    ids.add(chat_id)
    with open(_USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(ids), f)
