

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:  
    from .tracks import Track
    from .users import User


class ListeningSession:
    def __init__(
        self,
        session_id: str,
        user: User,
        track: Track,
        timestamp: datetime,
        duration_seconds: int,
    ) -> None:
        self.session_id = session_id
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_seconds = duration_seconds
        self.duration_listened_seconds = duration_seconds

    def duration_listened_minutes(self) -> float:
        return self.duration_seconds / 60
