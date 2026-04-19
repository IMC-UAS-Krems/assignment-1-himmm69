from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tracks import Track


class Artist:
    """Represents a music artist on the platform."""

    def __init__(self, artist_id: str, name: str, genre: str = "") -> None:
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks: list[Track] = []

    def track_count(self) -> int:
        return len(self.tracks)

    def add_track(self, track: Track) -> None:
        self.tracks.append(track)
