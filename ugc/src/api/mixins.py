from flask import current_app

from src.storages.base import Storage
from src.streamers.base import Streamer
from src.services.auth import username_required


class StorageMixin:
    """Миксин, добавляющий в класс атрибут storage."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage: Storage = current_app.config.get("storage")


class StreamerMixin:
    """Миксин, добавляющий в класс атрибут streamer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.streamer: Streamer = current_app.config.get("streamer")


class LoginMixin:
    """Миксин, добавляющий в класс атрибут username."""
    @username_required
    def __init__(self, username: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
