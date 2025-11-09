"""Chain of Responsibility implementation for authentication workflows."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional, Protocol


@dataclass
class AuthRequest:
    """Incoming authentication request with credentials and required permissions."""

    username: str
    password: str
    required_permissions: Iterable[str] = field(default_factory=tuple)
    session_token: Optional[str] = None


@dataclass
class AuthContext:
    """State shared across the authentication pipeline."""

    request: AuthRequest
    user_record: Optional[dict] = None
    permissions: set[str] = field(default_factory=set)
    session_data: Optional[dict] = None


@dataclass
class AuthResult:
    """Outcome returned by each handler in the chain."""

    success: bool
    message: str
    context: Optional[AuthContext] = None


class CredentialStore(Protocol):
    """Simple protocol abstraction used by the login handler."""

    def get_user(self, username: str) -> Optional[dict]:
        """Return user metadata, such as the password hash and assigned permissions."""


class SessionStore(Protocol):
    """Protocol abstraction used for session validation."""

    def get_session(self, token: str) -> Optional[dict]:
        """Return session metadata for the supplied token if it is still valid."""


class AuthHandler:
    """Abstract handler defining the Chain of Responsibility contract."""

    def __init__(self) -> None:
        self._next: Optional[AuthHandler] = None

    def set_next(self, handler: "AuthHandler") -> "AuthHandler":
        self._next = handler
        return handler

    def handle(self, context: AuthContext) -> AuthResult:
        """Execute the handler and delegate to the next one when appropriate."""

        result = self._process(context)
        if not result.success:
            return result

        if self._next is None:
            return result

        return self._next.handle(result.context or context)

    def _process(self, context: AuthContext) -> AuthResult:
        raise NotImplementedError


class LoginHandler(AuthHandler):
    """Concrete handler responsible for authenticating the user credentials."""

    def __init__(self, credential_store: CredentialStore) -> None:
        super().__init__()
        self._credential_store = credential_store

    def _process(self, context: AuthContext) -> AuthResult:
        user_record = self._credential_store.get_user(context.request.username)
        if user_record is None:
            return AuthResult(False, "Usuário não encontrado", context)

        if user_record.get("password") != context.request.password:
            return AuthResult(False, "Credenciais inválidas", context)

        context.user_record = user_record
        context.permissions = set(user_record.get("permissions", ()))
        return AuthResult(True, "Login bem-sucedido", context)


class PermissionHandler(AuthHandler):
    """Concrete handler that ensures the user has the required permissions."""

    def _process(self, context: AuthContext) -> AuthResult:
        missing = set(context.request.required_permissions) - context.permissions
        if missing:
            return AuthResult(
                False,
                f"Permissões ausentes: {', '.join(sorted(missing))}",
                context,
            )

        return AuthResult(True, "Permissões validadas", context)


class SessionValidationHandler(AuthHandler):
    """Concrete handler responsible for verifying the session token."""

    def __init__(self, session_store: SessionStore) -> None:
        super().__init__()
        self._session_store = session_store

    def _process(self, context: AuthContext) -> AuthResult:
        token = context.request.session_token
        if not token:
            return AuthResult(False, "Token de sessão ausente", context)

        session = self._session_store.get_session(token)
        if session is None:
            return AuthResult(False, "Sessão inválida ou expirada", context)

        context.session_data = session
        return AuthResult(True, "Sessão validada", context)
