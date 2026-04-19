from __future__ import annotations

from typing import TYPE_CHECKING

from .artists import Artist

if TYPE_CHECKING:
    from .tracks import AlbumTrack


class Album:
    """Represents a music album containing multiple tracks."""

    def __init__(
        self, album_id: str, title: str, artist: Artist, release_year: int
    ) -> None:
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks: list[AlbumTrack] = []

    def add_track(self, track: AlbumTrack) -> None:
        track.album = self
        self.tracks.append(track)
        self.tracks.sort(key=lambda t: t.track_number)

    def track_ids(self) -> set[str]:
        return {t.track_id for t in self.tracks}

    def duration_seconds(self) -> int:
        return int(sum(t.duration_seconds for t in self.tracks))
