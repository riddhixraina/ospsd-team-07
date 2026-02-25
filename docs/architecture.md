# Architecture

## Component Design

The project is split into two main components:

| Component | Purpose |
|-----------|---------|
| **issue_tracker_client_api** | Abstract interface: `Client`, `Issue`, `Board`, `Member` |
| **trello_client_impl** | Concrete implementation backed by the Trello REST API |

The interface defines the contract; the implementation provides the behavior. Consumers depend only on the interface and obtain the implementation via dependency injection.

## Interface Layer

### Client (ABC)

The `Client` abstract base class defines all operations:

- **Issue/card:** `get_issue`, `delete_issue`, `mark_complete`, `get_issues`
- **Board:** `get_board`, `get_boards`
- **Member:** `get_members_on_card`

### Data Types

| Type | Required Fields |
|------|-----------------|
| **Issue** | `id`, `title`, `isComplete` |
| **Board** | `id`, `name` |
| **Member** | `id`, `username`, `confirmed` |

## Implementation Layer

`trello_client_impl` provides:

- **TrelloClient** — Implements `Client` using Trello's Cards, Boards, and Members endpoints
- **TrelloCard** — Implements `Issue` with Trello card fields
- **TrelloBoard** — Implements `Board`
- **TrelloMember** — Implements `Member`

## Dependency Injection

Implementations register by replacing the factory at import time:

```python
# trello_client_impl/__init__.py
from trello_client_impl.trello_impl import register
register()  # Rebinds issue_tracker_client_api.get_client
```

Consumers import the implementation package first, then use the shared factory:

```python
import trello_client_impl  # Registers as get_client implementation
from issue_tracker_client_api import get_client

client = get_client(interactive=False)
```

## Authentication

The Trello implementation uses token-based auth:

- **Environment:** `TRELLO_API_KEY`, `TRELLO_TOKEN`
- **File:** `token.json` (key `"token"`) in the current directory
- **CI:** Set env vars in CircleCI Project Settings for e2e tests
