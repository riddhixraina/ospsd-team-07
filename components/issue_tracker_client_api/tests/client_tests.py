"""Unit tests for the Client abstract class."""

from abc import ABC

import pytest
from issue_tracker_client_api import Board, Issue, Member
from issue_tracker_client_api.client import Client, get_client


@pytest.mark.unit
class TestClientAbstractClass:
    """Test that Client is an abstract base class with required methods."""

    def test_client_is_abstract(self):
        """Test that Client cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            _ = Client()  # type: ignore

    def test_client_is_abc(self):
        """Test that Client is an ABC."""
        assert issubclass(Client, ABC)

    def test_client_has_required_methods(self):
        """Test that Client has all required abstract methods."""
        required_methods = [
            "get_issue",
            "delete_issue",
            "mark_complete",
            "get_issues",
            "get_board",
            "get_members_on_card",
        ]
        for method_name in required_methods:
            assert hasattr(Client, method_name)

    def test_concrete_client_implementation(self):
        """Test a concrete Client implementation."""

        class ConcreteClient(Client):
            """Concrete implementation of Client for testing."""

            def get_issue(self, issue_id: str) -> Issue:
                pass

            def delete_issue(self, issue_id: str) -> bool:
                return True

            def mark_complete(self, issue_id: str) -> bool:
                return True

            def get_issues(self, max_issues: int = 10):
                return iter([])

            def get_board(self, board_id: str) -> Board:
                pass

            def get_members_on_card(self, issue_id: str) -> list[Member]:
                return []

        client = ConcreteClient()
        assert client is not None
        assert isinstance(client, Client)


@pytest.mark.unit
class TestGetClientFactory:
    """Test the get_client factory function."""

    def test_get_client_not_implemented(self):
        """Test that get_client raises NotImplementedError."""
        with pytest.raises(NotImplementedError, match="Subclasses must implement"):
            get_client()

    def test_get_client_with_interactive_flag(self):
        """Test that get_client rejects interactive flag when not implemented."""
        with pytest.raises(NotImplementedError, match="Subclasses must implement"):
            get_client(interactive=True)
