"""Issue contract - Core issue representation."""

from abc import ABC, abstractmethod

class Issue(ABC):
    """Abstract base class representing an issue in the issue tracker."""
    
    @property
    @abstractmethod
    def id(self) -> str:
        """Return the unique identifier of the issue."""
        return NotImplementedError("Subclasses must implement id")
    
    @property
    @abstractmethod
    def title(self) -> str:
        """Return the title of the issue."""
        return NotImplementedError("Subclasses must implement title")
    
    @property
    @abstractmethod
    def priority(self) -> str:
        """Return the priority of the issue."""
        return NotImplementedError("Subclasses must implement priority")
    
    @property
    @abstractmethod
    def status(self) -> str:
        """Return the status of the issue."""
        return NotImplementedError("Subclasses must implement status")
    
    @property
    @abstractmethod
    def leader(self) -> str:
        """Return the leader of the issue."""
        return NotImplementedError("Subclasses must implement leader")
    
    
def get_issue(issue_id: str) -> Issue:
    """Return an issue by its ID.
    
    Args:
        issue_id: The ID of the issue to return.
    
    Returns:
        An instance of the Issue class with the given ID.
    """
    raise NotImplementedError("Subclasses must implement get_issue")