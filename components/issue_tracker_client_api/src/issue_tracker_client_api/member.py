"""Member contract - Compatible with Trello Member object."""

from abc import ABC, abstractmethod


class Member(ABC):
    """Abstract base class representing a member/user in the issue tracker.

    Maps to Trello's Member object.
    See: https://developer.atlassian.com/cloud/trello/guides/rest-api/object-definitions/#member-object
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """Return the unique identifier of the member."""
        raise NotImplementedError("Subclasses must implement id")

    @property
    @abstractmethod
    def username(self) -> str | None:
        """Username (Trello: username)."""
        raise NotImplementedError("Subclasses must implement username")

    @property
    @abstractmethod
    def confirmed(self) -> bool | None:
        """Whether the user has confirmed their email (Trello: confirmed)."""
        raise NotImplementedError("Subclasses must implement confirmed")
    
def get_member(member_id: str) -> Member:
    """Return a member by their ID."""
    raise NotImplementedError("Subclasses must implement get_member")
