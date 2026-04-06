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
    def __init__(self, album_id: str, title: str, artist: Artist) -> None:
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.tracks: list[AlbumTrack] = []

    def add_track(self, track: AlbumTrack) -> None:
        self.tracks.append(track)
