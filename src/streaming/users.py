from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .sessions import ListeningSession
    from .tracks import Track


class User:
    def __init__(self, user_id: str, name: str, age: int) -> None:
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions: list[ListeningSession] = []

    def add_session(self, session: ListeningSession) -> None:
        self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        return int(sum(s.duration_seconds for s in self.sessions))

    def total_listening_minutes(self) -> float:
        return self.total_listening_seconds() / 60

    def unique_tracks_listened(self) -> set[str]:
        return {s.track.track_id for s in self.sessions}


class FreeUser(User):
    pass


class PremiumUser(User):
    def __init__(
        self,
        user_id: str,
        name: str,
        age: int,
        subscription_start: datetime | None = None,
    ) -> None:
        super().__init__(user_id=user_id, name=name, age=age)
        self.subscription_start = subscription_start


class FamilyAccountUser(PremiumUser):
    def __init__(
        self,
        user_id: str,
        name: str,
        age: int,
        subscription_start: datetime | None = None,
    ) -> None:
        super().__init__(
            user_id=user_id,
            name=name,
            age=age,
            subscription_start=subscription_start,
        )
        self.sub_users: list[FamilyMember] = []

    def add_sub_user(self, member: FamilyMember) -> None:
        if member not in self.sub_users:
            self.sub_users.append(member)

    # keep backward-compatible name
    def add_member(self, member: FamilyMember) -> None:
        self.add_sub_user(member)

    def all_members(self) -> list[User]:
        return [self, *self.sub_users]


class FamilyMember(User):
    def __init__(
        self, user_id: str, name: str, age: int, parent: FamilyAccountUser
    ) -> None:
        super().__init__(user_id=user_id, name=name, age=age)
        self.parent = parent
