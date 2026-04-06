"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .artists import Artist

if TYPE_CHECKING:  # pragma: no cover
    from .tracks import AlbumTrack


class Album:
    def __init__(
        self, album_id: str, title: str, artist: Artist, release_year: int
    ) -> None:
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks: list[AlbumTrack] = []

    def add_track(self, track: AlbumTrack) -> None:
        # set back-reference
        track.album = self
        self.tracks.append(track)
        # keep ordered by track_number
        self.tracks.sort(key=lambda t: t.track_number)

    def track_ids(self) -> set[str]:
        return {t.track_id for t in self.tracks}

    def duration_seconds(self) -> int:
        return int(sum(t.duration_seconds for t in self.tracks))
