"""Board contract - Compatible with Trello Board object."""

from abc import ABC, abstractmethod


class Board(ABC):
    """Abstract base class representing a board in the issue tracker.

    Maps to Trello's Board object.
    See: https://developer.atlassian.com/cloud/trello/guides/rest-api/object-definitions/#board-object
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Return the unique identifier of the board."""
        raise NotImplementedError("Subclasses must implement id")

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the board."""
        raise NotImplementedError("Subclasses must implement name")
    

def get_board(board_id: str) -> Board:
    """Return a board by its ID."""
    raise NotImplementedError("Subclasses must implement get_board")

