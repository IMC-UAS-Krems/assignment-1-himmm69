

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING: 
    from .tracks import Track
    from .users import User


class Playlist:
    def __init__(self, playlist_id: str, name: str, owner: User) -> None:
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks: list[Track] = []

    def add_track(self, track: Track) -> None:
        
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track_id: str) -> None:
        self.tracks = [t for t in self.tracks if t.track_id != track_id]

    def total_duration_seconds(self) -> int:
        return int(sum(t.duration_seconds for t in self.tracks))


class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id: str, name: str, owner: User) -> None:
        super().__init__(playlist_id=playlist_id, name=name, owner=owner)
        # owner is always a contributor
        self.contributors: list[User] = [owner]

    def add_contributor(self, user: User) -> None:
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user: User) -> None:
        # never remove owner
        if user == self.owner:
            return
        if user in self.contributors:
            self.contributors.remove(user)
