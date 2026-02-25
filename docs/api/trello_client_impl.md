# Trello Client Implementation

Concrete implementation of the issue tracker API using the [Trello REST API](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/).

## Overview

`trello_client_impl` provides a concrete `issue_tracker_client_api.Client` backed by Trello's REST API. It returns `TrelloCard` (Issue), `TrelloBoard` (Board), and `TrelloMember` (Member) objects.

## TrelloClient

Implements `issue_tracker_client_api.Client`.

### Issue / Card methods

| Method | Trello API | Description |
|--------|------------|-------------|
| `get_issue(issue_id: str) -> Issue` | GET /cards/{id} | Single card |
| `delete_issue(issue_id: str) -> bool` | DEL /cards/{id} | Delete card |
| `mark_complete(issue_id: str) -> bool` | PUT /cards/{id} | Set card due complete |
| `get_issues(max_issues: int = 10) -> Iterator[Issue]` | GET /boards/{id}/cards | Cards on board |

### Board methods

| Method | Trello API | Description |
|--------|------------|-------------|
| `get_board(board_id: str) -> Board` | GET /boards/{id} | Single board |
| `get_boards() -> Iterator[Board]` | GET /members/me/boards | Current user's boards |

### Member methods

| Method | Trello API | Description |
|--------|------------|-------------|
| `get_members_on_card(issue_id: str) -> list[Member]` | GET /cards/{id}/members | Members on a card |

## Data Types

| Type | API contract | Description |
|-----|--------------|-------------|
| `TrelloCard` | `Issue` | Issue (id, title, isComplete) |
| `TrelloBoard` | `Board` | Board (id, name) |
| `TrelloMember` | `Member` | Member (id, username, confirmed) |

## Factory

- **`get_client_impl(*, interactive: bool = False) -> Client`** — Returns a `TrelloClient`. Assigned to `issue_tracker_client_api.get_client` on package import.

## Authentication

- **Environment:** `TRELLO_API_KEY`, `TRELLO_TOKEN`
- **File:** `token.json` (key `"token"`) in the current directory
- **Priority:** `TRELLO_TOKEN` → `token.json` → error if missing
