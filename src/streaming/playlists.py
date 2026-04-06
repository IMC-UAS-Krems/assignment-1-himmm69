"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .tracks import Track
    from .users import User


class Playlist:
    def __init__(self, playlist_id: str, name: str, owner: User) -> None:
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks: list[Track] = []

    def add_track(self, track: Track) -> None:
        self.tracks.append(track)


class CollaborativePlaylist(Playlist):
    def __init__(
        self,
        playlist_id: str,
        name: str,
        owner: User,
        contributors: list[User] | None = None,
    ) -> None:
        super().__init__(playlist_id=playlist_id, name=name, owner=owner)
        self.contributors: list[User] = (
            list(contributors) if contributors is not None else []
        )
