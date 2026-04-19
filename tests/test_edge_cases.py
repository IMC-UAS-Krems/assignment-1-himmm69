"""
test_edge_cases.py
------------------
Edge case tests for the StreamingPlatform implementation.
Tests empty inputs, invalid IDs, and boundary conditions.
"""

import pytest
from datetime import datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.artists import Artist
from streaming.albums import Album
from streaming.tracks import Song, AlbumTrack
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist


class TestEmptyPlatform:
    """Test behavior when platform has no data."""

    def test_all_users_empty(self) -> None:
        p = StreamingPlatform("Empty")
        assert p.all_users() == []

    def test_all_tracks_empty(self) -> None:
        p = StreamingPlatform("Empty")
        assert p.all_tracks() == []

    def test_all_playlists_empty(self) -> None:
        p = StreamingPlatform("Empty")
        assert p.all_playlists() == []

    def test_all_sessions_empty(self) -> None:
        p = StreamingPlatform("Empty")
        assert p.all_sessions() == []

    def test_total_listening_time_no_sessions(self) -> None:
        p = StreamingPlatform("Empty")
        now = datetime.now()
        result = p.total_listening_time_minutes(now - timedelta(days=1), now)
        assert result == 0.0

    def test_avg_unique_tracks_no_users(self) -> None:
        p = StreamingPlatform("Empty")
        assert p.avg_unique_tracks_per_premium_user() == 0.0

    def test_track_most_listeners_no_sessions(self) -> None:
        p = StreamingPlatform("Empty")
        assert p.track_with_most_distinct_listeners() is None

    def test_avg_session_duration_no_sessions(self) -> None:
        p = StreamingPlatform("Empty")
        assert p.avg_session_duration_by_user_type() == []

    def test_underage_listening_no_sessions(self) -> None:
        p = StreamingPlatform("Empty")
        assert p.total_listening_time_underage_sub_users_minutes() == 0.0

    def test_top_artists_no_sessions(self) -> None:
        p = StreamingPlatform("Empty")
        assert p.top_artists_by_listening_time() == []

    def test_collaborative_playlists_empty(self) -> None:
        p = StreamingPlatform("Empty")
        assert p.collaborative_playlists_with_many_artists() == []

    def test_avg_tracks_per_playlist_no_playlists(self) -> None:
        p = StreamingPlatform("Empty")
        result = p.avg_tracks_per_playlist_type()
        assert result["Playlist"] == 0.0
        assert result["CollaborativePlaylist"] == 0.0

    def test_users_completed_albums_empty(self) -> None:
        p = StreamingPlatform("Empty")
        assert p.users_who_completed_albums() == []


class TestInvalidIds:
    """Test behavior with invalid or nonexistent IDs."""

    def test_get_track_invalid_id(self) -> None:
        p = StreamingPlatform("Test")
        assert p.get_track("nonexistent") is None

    def test_get_user_invalid_id(self) -> None:
        p = StreamingPlatform("Test")
        assert p.get_user("nonexistent") is None

    def test_get_artist_invalid_id(self) -> None:
        p = StreamingPlatform("Test")
        assert p.get_artist("nonexistent") is None

    def test_get_album_invalid_id(self) -> None:
        p = StreamingPlatform("Test")
        assert p.get_album("nonexistent") is None

    def test_user_top_genre_invalid_user(self) -> None:
        p = StreamingPlatform("Test")
        assert p.user_top_genre("nonexistent") is None


class TestBoundaryConditions:
    """Test boundary conditions and edge values."""

    def test_top_artists_n_zero(self) -> None:
        p = StreamingPlatform("Test")
        assert p.top_artists_by_listening_time(n=0) == []

    def test_avg_unique_tracks_days_zero(self) -> None:
        p = StreamingPlatform("Test")
        user = PremiumUser("u1", "Test", 25)
        p.add_user(user)
        # With days=0, cutoff is now, so no sessions qualify
        assert p.avg_unique_tracks_per_premium_user(days=0) == 0.0

    def test_collaborative_threshold_zero(self) -> None:
        p = StreamingPlatform("Test")
        owner = FreeUser("u1", "Owner", 25)
        p.add_user(owner)

        artist = Artist("a1", "Artist1", "pop")
        p.add_artist(artist)

        song = Song("t1", "Song1", 180, "pop", artist)
        p.add_track(song)

        cp = CollaborativePlaylist("p1", "Collab", owner)
        cp.add_track(song)
        p.add_playlist(cp)

        # threshold=0 means >0 artists needed (1 artist qualifies)
        result = p.collaborative_playlists_with_many_artists(threshold=0)
        assert len(result) == 1

    def test_underage_threshold_zero(self) -> None:
        p = StreamingPlatform("Test")
        # With age_threshold=0, no one is under 0
        assert p.total_listening_time_underage_sub_users_minutes(age_threshold=0) == 0.0


class TestUserWithNoSessions:
    """Test user-related queries when user has no listening history."""

    def test_user_top_genre_no_sessions(self) -> None:
        p = StreamingPlatform("Test")
        user = FreeUser("u1", "Alice", 25)
        p.add_user(user)
        assert p.user_top_genre("u1") is None

    def test_user_unique_tracks_no_sessions(self) -> None:
        user = FreeUser("u1", "Alice", 25)
        assert user.unique_tracks_listened() == set()

    def test_user_total_listening_no_sessions(self) -> None:
        user = FreeUser("u1", "Alice", 25)
        assert user.total_listening_seconds() == 0
        assert user.total_listening_minutes() == 0.0


class TestAlbumEdgeCases:
    """Test album-related edge cases."""

    def test_empty_album_duration(self) -> None:
        artist = Artist("a1", "Test", "pop")
        album = Album("alb1", "Empty Album", artist, 2024)
        assert album.duration_seconds() == 0

    def test_empty_album_track_ids(self) -> None:
        artist = Artist("a1", "Test", "pop")
        album = Album("alb1", "Empty Album", artist, 2024)
        assert album.track_ids() == set()

    def test_album_not_completed_if_empty(self) -> None:
        p = StreamingPlatform("Test")
        artist = Artist("a1", "Test", "pop")
        p.add_artist(artist)

        album = Album("alb1", "Empty Album", artist, 2024)
        p.add_album(album)

        user = FreeUser("u1", "Alice", 25)
        p.add_user(user)

        # Empty albums should not count as completed
        result = p.users_who_completed_albums()
        assert result == []


class TestPlaylistEdgeCases:
    """Test playlist-related edge cases."""

    def test_empty_playlist_duration(self) -> None:
        owner = FreeUser("u1", "Owner", 25)
        playlist = Playlist("p1", "Empty", owner)
        assert playlist.total_duration_seconds() == 0

    def test_remove_nonexistent_track(self) -> None:
        owner = FreeUser("u1", "Owner", 25)
        playlist = Playlist("p1", "Test", owner)
        # Should not raise an error
        playlist.remove_track("nonexistent")
        assert playlist.tracks == []

    def test_add_duplicate_track(self) -> None:
        owner = FreeUser("u1", "Owner", 25)
        artist = Artist("a1", "Artist", "pop")
        song = Song("t1", "Song", 180, "pop", artist)

        playlist = Playlist("p1", "Test", owner)
        playlist.add_track(song)
        playlist.add_track(song)  # Duplicate

        assert len(playlist.tracks) == 1

    def test_remove_owner_from_collaborative(self) -> None:
        owner = FreeUser("u1", "Owner", 25)
        cp = CollaborativePlaylist("p1", "Collab", owner)

        cp.remove_contributor(owner)  # Should not remove owner
        assert owner in cp.contributors


class TestFreeUserAttributes:
    """Test FreeUser specific attributes."""

    def test_free_user_ad_supported(self) -> None:
        user = FreeUser("u1", "Free", 25)
        assert user.ad_supported is True


class TestFamilyAccountEdgeCases:
    """Test family account edge cases."""

    def test_add_duplicate_member(self) -> None:
        parent = FamilyAccountUser("p1", "Parent", 40)
        child = FamilyMember("c1", "Child", 10, parent)

        parent.add_sub_user(child)
        parent.add_sub_user(child)  # Duplicate

        assert len(parent.sub_users) == 1

    def test_all_members_includes_parent(self) -> None:
        parent = FamilyAccountUser("p1", "Parent", 40)
        members = parent.all_members()
        assert parent in members
