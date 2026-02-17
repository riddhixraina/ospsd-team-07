"""Core issue tracker client contract definitions and factory placeholder."""

from abc import ABC, abstractmethod
from collections.abc import Iterator

from issue_tracker_client_api.board import Board
from issue_tracker_client_api.issue import Issue
from issue_tracker_client_api.member import Member

__all__ = ["Client", "get_client"]


class Client(ABC):
    """Abstract base class representing an issue tracker client for managing issues."""

    @abstractmethod
    def get_issue(self, issue_id: str) -> Issue:
        """Return a single issue/card by its ID (Trello: GET /cards/{id})."""
        raise NotImplementedError("Subclasses must implement get_issue")

    @abstractmethod
    def delete_issue(self, issue_id: str) -> bool:
        """Delete an issue by its ID (Trello: DEL /cards/{id})."""
        raise NotImplementedError("Subclasses must implement delete_issue")

    @abstractmethod
    def mark_complete(self, issue_id: str) -> bool:
        """Mark an issue as complete (Trello: PUT /cards/{id} dueComplete=true)."""
        raise NotImplementedError("Subclasses must implement mark_complete")

    @abstractmethod
    def get_issues(self, max_issues: int = 10) -> Iterator[Issue]:
        """Return an iterator of issues, up to max_issues.

        Trello: GET /boards/{id}/cards.
        """
        raise NotImplementedError("Subclasses must implement get_issues")

    @abstractmethod
    def get_board(self, board_id: str) -> Board:
        """Return a single board by its ID (Trello: GET /boards/{id})."""
        raise NotImplementedError("Subclasses must implement get_board")

    @abstractmethod
    def get_boards(self) -> Iterator[Board]:
        """Return an iterator of boards for the authenticated user.

        Trello: GET /members/me/boards.
        """
        raise NotImplementedError("Subclasses must implement get_boards")

    @abstractmethod
    def get_members_on_card(self, issue_id: str) -> list[Member]:
        """Return members assigned to the card (Trello: GET /cards/{id}/members)."""
        raise NotImplementedError("Subclasses must implement get_members_on_card")


def get_client(*, interactive: bool = False) -> Client:
    """Return an instance of the concrete implementation of an issue tracker client."""
    raise NotImplementedError("Subclasses must implement get_client")
