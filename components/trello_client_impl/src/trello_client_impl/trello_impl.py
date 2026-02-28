"""Trello client implementation.

Concrete implementation of the issue tracker API using the Trello REST API.
See: https://developer.atlassian.com/cloud/trello/rest/api-group-cards/
"""

import json
import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any, TypedDict, cast

import issue_tracker_client_api
import requests
from issue_tracker_client_api import Board, Client, Issue, Member


class _TrelloCardResponse(TypedDict, total=False):
    id: str
    name: str
    dueComplete: bool
    desc: str | None
    due: str | None
    idBoard: str | None
    idList: str | None


class _TrelloBoardResponse(TypedDict, total=False):
    id: str
    name: str


class _TrelloMemberResponse(TypedDict, total=False):
    id: str
    username: str | None
    confirmed: bool | None


def _load_token() -> str | None:
    """Load token from TRELLO_TOKEN env or token.json (current directory)."""
    token = os.getenv("TRELLO_TOKEN")
    if token:
        return token
    token_path = Path.cwd() / "token.json"
    if token_path.is_file():
        with token_path.open(encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)
            return data.get("token")
    return None


class TrelloCard(Issue):
    """Concrete Issue built from Trello Card API response.

    Trello uses dueComplete for completion; we map it to is_complete.
    """

    def __init__(
        self,
        *,
        id: str,
        title: str = "",
        is_complete: bool = False,
        desc: str | None = None,
        due: str | None = None,
        id_board: str | None = None,
        id_list: str | None = None,
    ) -> None:
        self._id = id
        self._title = title
        self._is_complete = is_complete
        self._desc = desc
        self._due = due
        self._id_board = id_board
        self._id_list = id_list

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def is_complete(self) -> bool:
        return self._is_complete

    @property
    def desc(self) -> str | None:
        return self._desc

    @property
    def due(self) -> str | None:
        return self._due

    @property
    def id_board(self) -> str | None:
        return self._id_board

    @property
    def id_list(self) -> str | None:
        return self._id_list

    @classmethod
    def from_api(cls, card: _TrelloCardResponse) -> "TrelloCard":
        """Build TrelloCard from Trello API card object."""
        due_complete = bool(card.get("dueComplete", False))
        return cls(
            id=card["id"],
            title=card.get("name", ""),
            is_complete=due_complete,
            desc=card.get("desc") or None,
            due=card.get("due"),
            id_board=card.get("idBoard"),
            id_list=card.get("idList"),
        )


class TrelloBoard(Board):
    """Concrete Board built from Trello Board API response."""

    def __init__(
        self,
        *,
        id: str,
        name: str,
    ) -> None:
        self._id = id
        self._name = name

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def from_api(cls, board: _TrelloBoardResponse) -> "TrelloBoard":
        """Build TrelloBoard from Trello API board object."""
        return cls(
            id=board["id"],
            name=board.get("name", ""),
        )


class TrelloMember(Member):
    """Concrete Member built from Trello Member API response.

    Trello's 'confirmed' (email verified) maps to is_board_member.
    """

    def __init__(
        self,
        *,
        id: str,
        username: str | None = None,
        is_board_member: bool | None = None,
    ) -> None:
        self._id = id
        self._username = username
        self._is_board_member = is_board_member

    @property
    def id(self) -> str:
        return self._id

    @property
    def username(self) -> str | None:
        return self._username

    @property
    def is_board_member(self) -> bool | None:
        return self._is_board_member

    @classmethod
    def from_api(cls, member: _TrelloMemberResponse) -> "TrelloMember":
        """Build TrelloMember from Trello API member object."""
        confirmed = member.get("confirmed") if "confirmed" in member else None
        return cls(
            id=member["id"],
            username=member.get("username"),
            is_board_member=confirmed,
        )


# --- Trello Client ---

BASE = "https://api.trello.com/1"


class TrelloClient(Client):
    """Trello-backed implementation of the issue tracker Client."""

    def __init__(self, *, interactive: bool = False) -> None:
        self.interactive = interactive
        self.api_key = os.getenv("TRELLO_API_KEY", "")
        self._token = _load_token()
        self._default_board_id = os.getenv("TRELLO_BOARD_ID")

    @property
    def token(self) -> str:
        if not self._token:
            raise ValueError("Trello token not set. Set TRELLO_TOKEN or token.json.")
        return self._token

    def _query(self, **kwargs: str) -> dict[str, str]:
        return {"key": self.api_key, "token": self.token, **kwargs}

    def _get(
        self, path: str, params: dict[str, str] | None = None
    ) -> dict[str, Any] | list[Any]:
        url = f"{BASE}{path}" if path.startswith("/") else f"{BASE}/{path}"
        resp = requests.request(
            "GET",
            url,
            headers={"Accept": "application/json"},
            params=params or self._query(),
            timeout=30,
        )
        resp.raise_for_status()
        result: dict[str, Any] | list[Any] = resp.json()
        return result

    def _delete(self, path: str) -> None:
        url = f"{BASE}{path}" if path.startswith("/") else f"{BASE}/{path}"
        resp = requests.request(
            "DELETE",
            url,
            headers={"Accept": "application/json"},
            params=self._query(),
            timeout=30,
        )
        resp.raise_for_status()

    def _put(self, path: str, payload: dict[str, Any] | None = None) -> None:
        url = f"{BASE}{path}" if path.startswith("/") else f"{BASE}/{path}"
        resp = requests.request(
            "PUT",
            url,
            headers={"Accept": "application/json"},
            params=self._query(),
            json=payload or {},
            timeout=30,
        )
        resp.raise_for_status()

    def _post(self, path: str, params: dict[str, str] | None = None) -> None:
        url = f"{BASE}{path}" if path.startswith("/") else f"{BASE}/{path}"
        resp = requests.request(
            "POST",
            url,
            headers={"Accept": "application/json"},
            params={**self._query(), **(params or {})},
            timeout=30,
        )
        resp.raise_for_status()

    def get_issue(self, issue_id: str) -> Issue:
        data = self._get(f"/cards/{issue_id}")
        if not isinstance(data, dict):
            raise TypeError("Expected dict from cards API")
        return TrelloCard.from_api(cast("_TrelloCardResponse", data))

    def delete_issue(self, issue_id: str) -> bool:
        # Trello requires archiving before delete
        self._put(f"/cards/{issue_id}", payload={"closed": True})
        self._delete(f"/cards/{issue_id}")
        return True

    def mark_complete(self, issue_id: str) -> bool:
        self._put(f"/cards/{issue_id}", payload={"dueComplete": True})
        return True

    def update_status(self, issue_id: str, status: str) -> bool:
        # Map provider-agnostic status to Trello: complete -> dueComplete
        if status == "complete":
            self._put(f"/cards/{issue_id}", payload={"dueComplete": True})
        elif status == "in_progress":
            self._put(f"/cards/{issue_id}", payload={"dueComplete": False})
        # 'todo' and others: Trello has no direct equivalent, no-op
        return True

    def get_issues(self, max_issues: int = 10) -> Iterator[Issue]:
        board_id = self._default_board_id
        if not board_id:
            boards = self._get("/members/me/boards")
            if not isinstance(boards, list) or not boards:
                return
            first: dict[str, Any] = boards[0]
            board_id = first["id"]
        data = self._get(f"/boards/{board_id}/cards")
        if not isinstance(data, list):
            return
        for count, card in enumerate(data):
            if count >= max_issues:
                break
            if isinstance(card, dict):
                yield TrelloCard.from_api(cast("_TrelloCardResponse", card))

    def get_board(self, board_id: str) -> Board:
        data = self._get(f"/boards/{board_id}")
        if not isinstance(data, dict):
            raise TypeError("Expected dict from boards API")
        return TrelloBoard.from_api(cast("_TrelloBoardResponse", data))

    def get_boards(self) -> Iterator[Board]:
        data = self._get("/members/me/boards")
        if not isinstance(data, list):
            return
        for board in data:
            if isinstance(board, dict):
                yield TrelloBoard.from_api(cast("_TrelloBoardResponse", board))

    def get_members_on_card(self, issue_id: str) -> list[Member]:
        data = self._get(f"/cards/{issue_id}/members")
        if not isinstance(data, list):
            return []
        return [
            TrelloMember.from_api(cast("_TrelloMemberResponse", m))
            for m in data
            if isinstance(m, dict)
        ]

    def assign_issue(self, issue_id: str, member_id: str) -> bool:
        self._post(f"/cards/{issue_id}/idMembers", params={"idMember": member_id})
        return True


def get_client_impl(*, interactive: bool = False) -> Client:
    """Return an instance of the Trello client."""
    return TrelloClient(interactive=interactive)


def register() -> None:
    """Register the Trello client with the issue tracker client API."""
    issue_tracker_client_api.get_client = get_client_impl
