"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .artists import Artist

if TYPE_CHECKING:  # pragma: no cover
    from .albums import Album


class Track:
    def __init__(
        self, track_id: str, title: str, duration_seconds: int, genre: str
    ) -> None:
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def duration_minutes(self) -> float:
        return self.duration_seconds / 60

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Track):
            return False
        return self.track_id == other.track_id

    def __hash__(self) -> int:
        return hash(self.track_id)


class Song(Track):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        artist: Artist,
    ) -> None:
        super().__init__(
            track_id=track_id,
            title=title,
            duration_seconds=duration_seconds,
            genre=genre,
        )
        self.artist = artist


class SingleRelease(Song):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        artist: Artist,
        release_date: Any,
    ) -> None:
        super().__init__(
            track_id=track_id,
            title=title,
            duration_seconds=duration_seconds,
            genre=genre,
            artist=artist,
        )
        self.release_date = release_date


class AlbumTrack(Song):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        artist: Artist,
        track_number: int,
    ) -> None:
        super().__init__(
            track_id=track_id,
            title=title,
            duration_seconds=duration_seconds,
            genre=genre,
            artist=artist,
        )
        self.track_number = track_number
        self.album: Album | None = None


class Podcast(Track):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        host: str = "",
    ) -> None:
        super().__init__(
            track_id=track_id,
            title=title,
            duration_seconds=duration_seconds,
            genre=genre,
        )
        self.host = host


class InterviewEpisode(Podcast):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        host: str = "",
        guest: str = "",
    ) -> None:
        super().__init__(
            track_id=track_id,
            title=title,
            duration_seconds=duration_seconds,
            genre=genre,
            host=host,
        )
        self.guest = guest


class NarrativeEpisode(Podcast):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        host: str = "",
        narrator: str = "",
        series_name: str = "",
    ) -> None:
        super().__init__(
            track_id=track_id,
            title=title,
            duration_seconds=duration_seconds,
            genre=genre,
            host=host,
        )
        self.narrator = narrator
        self.series_name = series_name


class AudiobookTrack(Track):
    def __init__(
        self,
        track_id: str,
        title: str,
        duration_seconds: int,
        genre: str,
        author: str,
        chapter_number: int,
    ) -> None:
        super().__init__(
            track_id=track_id,
            title=title,
            duration_seconds=duration_seconds,
            genre=genre,
        )
        self.author = author
        self.chapter_number = chapter_number
