"""Trello client implementation.

Concrete implementation of the issue tracker API using the Trello REST API.
Maps Issue ↔ Card, Board ↔ Board, Member ↔ Member per Trello object definitions.
See: https://developer.atlassian.com/cloud/trello/rest/api-group-cards/
     https://developer.atlassian.com/cloud/trello/guides/rest-api/object-definitions/
"""

import os
from collections.abc import Iterator

import requests

import issue_tracker_client_api
from issue_tracker_client_api import Client, Board, Issue, Member


def _load_token() -> str | None:
    """Load token from TRELLO_TOKEN env or token.json (current directory)."""
    token = os.getenv("TRELLO_TOKEN")
    if token:
        return token
    token_path = os.path.join(os.getcwd(), "token.json")
    if os.path.isfile(token_path):
        with open(token_path, encoding="utf-8") as f:
            import json

            data = json.load(f)
            return data.get("token")
    return None


class TrelloCard(Issue):
    """Concrete Issue built from Trello Card API response."""

    def __init__(
        self,
        *,
        id: str,
        title: str = "",
        isComplete: bool = False,
        dueComplete: bool = False,
        desc: str | None = None,
        due: str | None = None,
        idBoard: str | None = None,
        idList: str | None = None,
    ) -> None:
        self._id = id
        self._title = title
        self._isComplete = isComplete or dueComplete
        self._dueComplete = dueComplete
        self._desc = desc
        self._due = due
        self._idBoard = idBoard
        self._idList = idList

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def isComplete(self) -> bool:
        return self._isComplete

    @property
    def dueComplete(self) -> bool:
        return self._dueComplete

    @property
    def desc(self) -> str | None:
        return self._desc

    @property
    def due(self) -> str | None:
        return self._due

    @property
    def id_board(self) -> str | None:
        return self._idBoard

    @property
    def id_list(self) -> str | None:
        return self._idList

    @classmethod
    def from_api(cls, card: dict) -> "TrelloCard":
        """Build TrelloCard from Trello API card object."""
        return cls(
            id=card["id"],
            title=card.get("name", ""),
            isComplete=bool(card.get("dueComplete", False)),
            desc=card.get("desc") or None,
            due=card.get("due"),
            idBoard=card.get("idBoard"),
            idList=card.get("idList"),
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
    def from_api(cls, board: dict) -> "TrelloBoard":
        return cls(
            id=board["id"],
            name=board.get("name", ""),
        )


class TrelloMember(Member):
    """Concrete Member built from Trello Member API response."""

    def __init__(
        self,
        *,
        id: str,
        username: str | None = None,
        confirmed: bool | None = None,
    ) -> None:
        self._id = id
        self._username = username
        self._confirmed = confirmed

    @property
    def id(self) -> str:
        return self._id

    @property
    def username(self) -> str | None:
        return self._username

    @property
    def confirmed(self) -> bool | None:
        return self._confirmed

    @classmethod
    def from_api(cls, member: dict) -> "TrelloMember":
        return cls(
            id=member["id"],
            username=member.get("username"),
            confirmed=member.get("confirmed") if "confirmed" in member else None,
        )


# --- Trello Client ---

BASE = "https://api.trello.com/1"


class TrelloClient(Client):
    """Trello-backed implementation of the issue tracker Client."""

    def __init__(self, interactive: bool = False) -> None:
        self.interactive = interactive
        self.api_key = os.getenv("TRELLO_API_KEY", "")
        self._token = _load_token()
        self._default_board_id = os.getenv("TRELLO_BOARD_ID")

    @property
    def token(self) -> str:
        if not self._token:
            raise ValueError(
                "Trello token not set. Set TRELLO_TOKEN or create token.json with a 'token' key."
            )
        return self._token

    def _query(self, **kwargs: str) -> dict:
        return {"key": self.api_key, "token": self.token, **kwargs}

    def _get(self, path: str, params: dict | None = None) -> dict | list:
        url = f"{BASE}{path}" if path.startswith("/") else f"{BASE}/{path}"
        resp = requests.request(
            "GET",
            url,
            headers={"Accept": "application/json"},
            params=params or self._query(),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

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

    def _put(self, path: str, json: dict | None = None) -> None:
        url = f"{BASE}{path}" if path.startswith("/") else f"{BASE}/{path}"
        resp = requests.request(
            "PUT",
            url,
            headers={"Accept": "application/json"},
            params=self._query(),
            json=json or {},
            timeout=30,
        )
        resp.raise_for_status()

    def get_issue(self, issue_id: str) -> Issue:
        data = self._get(f"/cards/{issue_id}")
        return TrelloCard.from_api(data)

    def delete_issue(self, issue_id: str) -> bool:
        self._delete(f"/cards/{issue_id}")
        return True

    def mark_complete(self, issue_id: str) -> bool:
        self._put(f"/cards/{issue_id}", json={"dueComplete": True})
        return True

    def get_issues(self, max_issues: int = 10) -> Iterator[Issue]:
        board_id = self._default_board_id
        if not board_id:
            boards = self._get("/members/me/boards")
            if not boards:
                return iter([])
            board_id = boards[0]["id"]
        data = self._get(f"/boards/{board_id}/cards")
        count = 0
        for card in data:
            if count >= max_issues:
                break
            yield TrelloCard.from_api(card)
            count += 1

    def get_board(self, board_id: str) -> Board:
        data = self._get(f"/boards/{board_id}")
        return TrelloBoard.from_api(data)

    def get_boards(self) -> Iterator[Board]:
        data = self._get("/members/me/boards")
        for board in data:
            yield TrelloBoard.from_api(board)

    def get_members_on_card(self, issue_id: str) -> list[Member]:
        data = self._get(f"/cards/{issue_id}/members")
        return [TrelloMember.from_api(m) for m in data]


def get_client_impl(*, interactive: bool = False) -> Client:
    """Return an instance of the Trello client."""
    return TrelloClient(interactive=interactive)


def register() -> None:
    """Register the Trello client with the issue tracker client API."""
    issue_tracker_client_api.get_client = get_client_impl
