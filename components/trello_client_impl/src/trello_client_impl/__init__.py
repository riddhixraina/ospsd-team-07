"""Public exports for the Issue Tracker client implementation package."""

from trello_client_impl.trello_impl import (
    TrelloBoard as TrelloBoard,
)
from trello_client_impl.trello_impl import (
    TrelloCard as TrelloCard,
)
from trello_client_impl.trello_impl import (
    TrelloClient as TrelloClient,
)
from trello_client_impl.trello_impl import (
    TrelloMember as TrelloMember,
)
from trello_client_impl.trello_impl import (
    get_client_impl as get_client_impl,
)
from trello_client_impl.trello_impl import (
    register,
)

# Dependency Injection happens at import time
register()
