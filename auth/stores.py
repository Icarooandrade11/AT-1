"""In-memory stores used by the authentication chain for demonstration purposes."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional


@dataclass
class InMemoryCredentialStore:
    """Simple credential repository using a Python dictionary."""

    users: Dict[str, dict]

    def get_user(self, username: str) -> Optional[dict]:
        return self.users.get(username)


@dataclass
class InMemorySessionStore:
    """Session store that considers expiration timestamps."""

    sessions: Dict[str, dict]

    def get_session(self, token: str) -> Optional[dict]:
        session = self.sessions.get(token)
        if session is None:
            return None

        expires_at: datetime = session.get("expires_at", datetime.min)
        if datetime.utcnow() > expires_at:
            return None

        return session

    @classmethod
    def issue_session(cls, token: str, user: dict, ttl_seconds: int = 3600) -> "InMemorySessionStore":
        """Helper method to build a store with a single session entry."""

        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
        session = {"user": user, "expires_at": expires_at}
        return cls({token: session})
