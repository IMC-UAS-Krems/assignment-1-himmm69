"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .tracks import Track
    from .users import User


class ListeningSession:
    def __init__(
        self, user: User, track: Track, timestamp: datetime, duration_seconds: int
    ) -> None:
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_seconds = duration_seconds
