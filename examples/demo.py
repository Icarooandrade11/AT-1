"""Demonstração do uso da cadeia de autenticação."""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Garante que o pacote ``auth`` seja encontrado quando o script for executado diretamente.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from auth import (  # noqa: E402  # import after path adjustment
    AuthContext,
    AuthRequest,
    InMemoryCredentialStore,
    InMemorySessionStore,
    LoginHandler,
    PermissionHandler,
    SessionValidationHandler,
)


def build_chain():
    credential_store = InMemoryCredentialStore(
        {
            "alice": {
                "password": "senha123",
                "permissions": {"admin", "feature:read"},
            }
        }
    )

    session_store = InMemorySessionStore(
        {
            "token-abc": {
                "user": "alice",
                "expires_at": datetime.utcnow() + timedelta(hours=1),
            }
        }
    )

    login = LoginHandler(credential_store)
    permissions = PermissionHandler()
    session = SessionValidationHandler(session_store)

    login.set_next(permissions).set_next(session)
    return login


def main() -> None:
    chain = build_chain()
    request = AuthRequest(
        username="alice",
        password="senha123",
        required_permissions={"admin"},
        session_token="token-abc",
    )
    context = AuthContext(request=request)
    result = chain.handle(context)
    print(result)


if __name__ == "__main__":
    main()
