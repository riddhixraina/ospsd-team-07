# Trello Client Implementation

## Overview

`trello_client_impl` provides a concrete `issue_tracker_client_api.Client` backed by the [Trello REST API](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/). It returns `TrelloCard` (Issue), `TrelloBoard` (Board), and `TrelloMember` (Member) objects that align with [Trello's object definitions](https://developer.atlassian.com/cloud/trello/guides/rest-api/object-definitions/).

## Purpose

- **Trello API integration:** Uses Trello's Cards, Boards, and Members endpoints.
- **Token-based auth:** Authenticates via API key + token (environment or `token.json`).
- **Full Client implementation:** Implements all abstract `Client` methods (issues, boards, members).
- **Dependency injection:** Registers itself as the `get_client` implementation on import.

## Architecture

### Authentication

- **`interactive=False`:** Use environment variables or existing `token.json`. Preferred for CI/CD and scripts.
- **`interactive=True`:** Reserved for future browser OAuth flow; currently same as above.

**Credential priority:** `TRELLO_TOKEN` → `token.json` (current directory, key `"token"`) → error if missing.

**Required environment variables:**

- `TRELLO_API_KEY` – Your Trello API key.
- `TRELLO_TOKEN` – Your Trello token (or provide via `token.json`).

### Dependency injection

```python
import trello_client_impl  # rebinds the factory

from issue_tracker_client_api import get_client
client = get_client(interactive=False)
```

## API Reference

### Types

| Type          | API contract        | Description                                      |
|---------------|---------------------|--------------------------------------------------|
| `TrelloCard`  | `Issue`             | Issue (id, title, isComplete) |
| `TrelloBoard` | `Board`             | Board (id, name)       |
| `TrelloMember`| `Member`            | Member (id, username, confirmed) |

### TrelloClient

Implements `issue_tracker_client_api.Client`.

#### Issue / Card methods

- **`get_issue(issue_id: str) -> Issue`** – Single card (GET /cards/{id}).
- **`delete_issue(issue_id: str) -> bool`** – Delete card (DEL /cards/{id}).
- **`mark_complete(issue_id: str) -> bool`** – Set card due complete (PUT /cards/{id}).
- **`get_issues(max_issues: int = 10) -> Iterator[Issue]`** – Cards on board (GET /boards/{id}/cards).

#### Board methods

- **`get_board(board_id: str) -> Board`** – Single board (GET /boards/{id}).
- **`get_boards() -> Iterator[Board]`** – Current user’s boards (GET /members/me/boards).

#### Member methods

- **`get_members_on_card(issue_id: str) -> list[Member]`** – Members on a card (GET /cards/{id}/members).

### Factory

- **`get_client_impl(*, interactive: bool = False) -> Client`** – Returns a `TrelloClient` and is assigned to `issue_tracker_client_api.get_client` on import.

## Usage examples

### Basic issue retrieval

```python
import trello_client_impl
from issue_tracker_client_api import get_client

client = get_client(interactive=False)
for issue in client.get_issues(max_issues=3):
    print(f"{issue.id}: {issue.title} (complete={issue.isComplete})")
```

### Card with Trello fields

```python
import trello_client_impl
from issue_tracker_client_api import get_client

client = get_client(interactive=False)
issue = client.get_issue("card-id")
print(issue.title)
```

### Boards and members

```python
import trello_client_impl
from issue_tracker_client_api import get_client

client = get_client(interactive=False)
for board in client.get_boards():
    print(board.id, board.name, board.url)
b = client.get_board("board-id")

members = client.get_members_on_card("card-id")
for m in members:
    print(m.id, m.username)
```