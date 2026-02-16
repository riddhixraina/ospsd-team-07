"""Public exports for the Issue Tracker client implementation package."""

from trello_client_impl.trello_impl import (
    TrelloBoard,
    TrelloCard,
    TrelloClient,
    TrelloMember,
    get_client_impl,
    register,
)

__all__ = [
    "TrelloBoard",
    "TrelloCard",
    "TrelloClient",
    "TrelloMember",
    "get_client_impl",
    "register",
]

# Dependency Injection happens at import time
register()
