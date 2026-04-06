"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

from __future__ import annotations


class Artist:
    def __init__(self, artist_id: str, name: str) -> None:
        self.artist_id = artist_id
        self.name = name
