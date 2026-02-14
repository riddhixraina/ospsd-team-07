"""Core issue tracker client contract definitions and factory placeholder."""

from abc import ABC, abstractmethod
from collections.abc import Iterator

from issue_tracker_client_api.issue import Issue

__all__ = ["Client", "get_client"]

class Client(ABC):
    """Abstract base class representing an issue tracker client for managing issues."""
    
    @abstractmethod
    def get_issue(self, issue_id: str) -> Issue:
        """Return a single issue by its ID."""
        raise NotImplementedError("Subclasses must implement get_issue")
    
    @abstractmethod
    def delete_issue(self, issue_id:str) -> bool:
        """Delete an issue by its ID."""
        raise NotImplementedError("Subclasses must implement delete_issue")
    
    @abstractmethod
    def assign_priority(self, issue_id: str, priority: str) -> bool:
        """Assign a priority label to an issue."""
        raise NotImplementedError("Subclasses must implement assign_priority")
    
    @abstractmethod
    def assign_leader(self, issue_id: str, leader: str) -> bool:
        """Assign a leader to an issue."""
        raise NotImplementedError("Subclasses must implement assign_leader")
    
    @abstractmethod
    def assign_status(self, issue_id: str, status: str) -> bool:
        """Assign a status to an issue."""
        raise NotImplementedError("Subclasses must implement assign_status")
    
    @abstractmethod
    def get_issues(self, max_issues: int = 10) -> Iterator[Issue]:
        """Return an iterator of issues, up to max_issues."""
        raise NotImplementedError("Subclasses must implement get_issues")
    
def get_client(*, interactive: bool = False) -> Client:
    """Return an instance of the concrete implementation of an issue tracker client."""
    raise NotImplementedError("Subclasses must implement get_client")