"""Implementation of the List contract."""

from typing import TypedDict

from issue_tracker_client_api import List as ListContract


class _TrelloListResponse(TypedDict, total=False):
    id: str
    name: str


class TrelloList(ListContract):
    """Concrete List built from Trello lists API response."""

    def __init__(self, *, id: str, name: str) -> None:
        self._id = id
        self._name = name

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def from_api(cls, list_obj: _TrelloListResponse) -> "TrelloList":
        """Build List from API list object."""
        return cls(
            id=list_obj["id"],
            name=list_obj.get("name", ""),
        )
