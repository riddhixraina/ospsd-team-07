"""Issue (Card) contract - Core issue representation compatible with Trello Card."""

from abc import ABC, abstractmethod


class Issue(ABC):
    """Abstract base class representing an issue/card in the issue tracker.

    Aligns with Trello's Card object where applicable. Required: id, title, isComplete.
    Optional fields (desc, due, id_board, etc.) map to Trello Card;
    return None if unsupported.
    See: https://developer.atlassian.com/cloud/trello/guides/rest-api/object-definitions/#card-object
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Return the unique identifier of the issue (Trello: card id)."""
        raise NotImplementedError("Subclasses must implement id")

    @property
    @abstractmethod
    def title(self) -> str:
        """Return the title of the issue (Trello: card name)."""
        raise NotImplementedError("Subclasses must implement title")

    @property
    @abstractmethod
    def isComplete(self) -> bool:
        """Return whether the issue is complete (Trello: card dueComplete)."""
        raise NotImplementedError("Subclasses must implement isComplete")


def get_issue(issue_id: str) -> Issue:
    """Return an issue by its ID.

    Args:
        issue_id: The ID of the issue to return.

    Returns:
        An instance of the Issue class with the given ID.

    """
    raise NotImplementedError("Subclasses must implement get_issue")
