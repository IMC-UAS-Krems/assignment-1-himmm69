from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from .tracks import Song
from .users import FamilyMember, PremiumUser

if TYPE_CHECKING:
    from .albums import Album
    from .artists import Artist
    from .playlists import Playlist, CollaborativePlaylist
    from .sessions import ListeningSession
    from .tracks import Track
    from .users import User


class StreamingPlatform:
    def __init__(self, name: str) -> None:
        self.name = name

        self._tracks: dict[str, Track] = {}
        self._users: dict[str, User] = {}
        self._artists: dict[str, Artist] = {}
        self._albums: dict[str, Album] = {}
        self._playlists: list[Playlist] = []
        self._sessions: list[ListeningSession] = []

    def add_track(self, track: Track) -> None:
        self._tracks[track.track_id] = track

    def add_user(self, user: User) -> None:
        self._users[user.user_id] = user

    def add_artist(self, artist: Artist) -> None:
        self._artists[artist.artist_id] = artist

    def add_album(self, album: Album) -> None:
        self._albums[album.album_id] = album

    def add_playlist(self, playlist: Playlist) -> None:
        self._playlists.append(playlist)

    def record_session(self, session: ListeningSession) -> None:
        self._sessions.append(session)

        session.user.add_session(session)

    def get_track(self, track_id: str) -> Track | None:
        return self._tracks.get(track_id)

    def get_user(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def get_artist(self, artist_id: str) -> Artist | None:
        return self._artists.get(artist_id)

    def get_album(self, album_id: str) -> Album | None:
        return self._albums.get(album_id)

    def all_users(self) -> list[User]:
        return list(self._users.values())

    def all_tracks(self) -> list[Track]:
        return list(self._tracks.values())

    def all_playlists(self) -> list[Playlist]:
        return self._playlists

    def all_sessions(self) -> list[ListeningSession]:
        return self._sessions

    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        total_seconds = 0
        for s in self._sessions:
            if start <= s.timestamp <= end:
                total_seconds += s.duration_seconds
        return total_seconds / 60

    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        premium_users = [u for u in self._users.values() if type(u) is PremiumUser]
        if not premium_users:
            return 0.0

        cutoff = datetime.now() - timedelta(days=days)
        per_user_counts: list[int] = []
        for u in premium_users:
            unique_tracks = {s.track for s in u.sessions if s.timestamp >= cutoff}
            per_user_counts.append(len(unique_tracks))

        return sum(per_user_counts) / len(per_user_counts)

    def track_with_most_distinct_listeners(self):
        if not self._sessions:
            return None

        listeners_by_track: dict[object, set[object]] = defaultdict(set)
        for s in self._sessions:
            listeners_by_track[s.track].add(s.user)

        return max(listeners_by_track.items(), key=lambda kv: len(kv[1]))[0]

    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        durations: dict[str, list[int]] = defaultdict(list)
        for s in self._sessions:
            durations[type(s.user).__name__].append(s.duration_seconds)

        result: list[tuple[str, float]] = []
        for type_name, ds in durations.items():
            result.append((type_name, (sum(ds) / len(ds)) if ds else 0.0))

        result.sort(key=lambda t: t[1], reverse=True)
        return result

    def total_listening_time_underage_sub_users_minutes(
        self, age_threshold: int = 18
    ) -> float:
        total_seconds = 0
        for s in self._sessions:
            if isinstance(s.user, FamilyMember) and s.user.age < age_threshold:
                total_seconds += s.duration_seconds
        return total_seconds / 60

    def top_artists_by_listening_time(self, n: int = 5):
        minutes_by_artist: dict[object, int] = defaultdict(int)
        for s in self._sessions:
            if isinstance(s.track, Song):
                minutes_by_artist[s.track.artist] += s.duration_seconds
        ranked = sorted(
            ((artist, secs / 60) for artist, secs in minutes_by_artist.items()),
            key=lambda t: t[1],
            reverse=True,
        )
        return ranked[:n]

    def user_top_genre(self, user_id: str):
        user = self.get_user(user_id)
        if user is None or not user.sessions:
            return None
        seconds_by_genre: dict[str, int] = defaultdict(int)
        total = 0
        for s in user.sessions:
            seconds_by_genre[s.track.genre] += s.duration_seconds
            total += s.duration_seconds
        if total == 0:
            return None
        top_genre = max(seconds_by_genre.items(), key=lambda kv: kv[1])[0]
        pct = (seconds_by_genre[top_genre] / total) * 100
        return (top_genre, pct)

    def collaborative_playlists_with_many_artists(self, threshold: int = 3):
        result = []
        for p in self._playlists:
            if p.__class__.__name__ != "CollaborativePlaylist":
                continue
            artists = {t.artist for t in p.tracks if isinstance(t, Song)}
            if len(artists) > threshold:
                result.append(p)
        return result

    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        total_playlist = 0
        count_playlist = 0
        total_collab = 0
        count_collab = 0
        for p in self._playlists:
            if p.__class__.__name__ == "CollaborativePlaylist":
                total_collab += len(p.tracks)
                count_collab += 1
            else:
                total_playlist += len(p.tracks)
                count_playlist += 1
        return {
            "Playlist": (total_playlist / count_playlist) if count_playlist else 0.0,
            "CollaborativePlaylist": (
                (total_collab / count_collab) if count_collab else 0.0
            ),
        }

    def users_who_completed_albums(self):
        # Minimal implementation: for each user, check albums where they listened to all track_ids
        result = []
        for u in self.all_users():
            listened_ids = {s.track.track_id for s in u.sessions}
            completed_titles: list[str] = []
            for album in self._albums.values():
                if not album.tracks:
                    continue
                album_ids = {t.track_id for t in album.tracks}
                if album_ids.issubset(listened_ids):
                    completed_titles.append(album.title)
            if completed_titles:
                result.append((u, completed_titles))
        return result
