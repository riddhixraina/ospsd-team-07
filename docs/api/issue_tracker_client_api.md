# Issue Tracker Client API

Abstract interface for an issue tracker client. Defines the `Client` ABC and data types (`Issue`, `Board`, `Member`).

## Overview

`issue_tracker_client_api` defines the abstract interface for an issue tracker client. Implementations (e.g. `trello_client_impl`) provide the concrete logic. The design is compatible with [Trello's REST API](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/) and [object definitions](https://developer.atlassian.com/cloud/trello/guides/rest-api/object-definitions/).

## Client (abstract)

```python
class Client(ABC):
    def get_issue(self, issue_id: str) -> Issue: ...
    def delete_issue(self, issue_id: str) -> bool: ...
    def mark_complete(self, issue_id: str) -> bool: ...
    def get_issues(self, max_issues: int = 10) -> Iterator[Issue]: ...
    def get_board(self, board_id: str) -> Board: ...
    def get_boards(self) -> Iterator[Board]: ...
    def get_members_on_card(self, issue_id: str) -> list[Member]: ...
```

| Method | Description |
|--------|-------------|
| `get_issue(issue_id)` | Return a single issue/card by ID |
| `delete_issue(issue_id)` | Remove the issue |
| `mark_complete(issue_id)` | Mark the issue complete (e.g. Trello `dueComplete`) |
| `get_issues(max_issues)` | Yield issues/cards, up to `max_issues` |
| `get_board(board_id)` | Return a board by ID |
| `get_boards()` | Yield boards (e.g. current user's boards) |
| `get_members_on_card(issue_id)` | Return members assigned to the card |

## Data Types

| Type | Required Fields |
|------|-----------------|
| **Issue** | `id`, `title`, `isComplete` |
| **Board** | `id`, `name` |
| **Member** | `id`, `username`, `confirmed` |

## Factory

```python
def get_client(*, interactive: bool = False) -> Client
```

Returns the registered implementation or raises `NotImplementedError` if none. Implementations register at import time (see [Architecture](../architecture.md#dependency-injection)).
