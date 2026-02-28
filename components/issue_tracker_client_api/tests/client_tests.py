"""Unit tests for the Client abstract class."""

from abc import ABC
from collections.abc import Iterator

import pytest
from issue_tracker_client_api import Board, Issue, List, Member
from issue_tracker_client_api.client import Client, get_client


@pytest.mark.unit
class TestClientAbstractClass:
    """Test that Client is an abstract base class with required methods."""

    def test_client_is_abstract(self) -> None:
        """Test that Client cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            _ = Client()  # type: ignore[abstract]

    def test_client_is_abc(self) -> None:
        """Test that Client is an ABC."""
        assert issubclass(Client, ABC)

    def test_client_has_required_methods(self) -> None:
        """Test that Client has all required abstract methods."""
        required_methods = [
            "get_issue",
            "delete_issue",
            "mark_complete",
            "update_status",
            "get_issues",
            "get_board",
            "get_boards",
            "get_lists",
            "get_members_on_card",
            "assign_issue",
            "create_issue",
        ]
        for method_name in required_methods:
            assert hasattr(Client, method_name)

    def test_concrete_client_implementation(self) -> None:
        """Test a concrete Client implementation."""

        class ConcreteClient(Client):
            """Concrete implementation of Client for testing."""

            def get_issue(self, issue_id: str) -> Issue:  # type: ignore[empty-body]
                ...

            def delete_issue(self, issue_id: str) -> bool:
                return True

            def mark_complete(self, issue_id: str) -> bool:
                return True

            def update_status(self, issue_id: str, status: str) -> bool:
                return True

            def get_issues(self, max_issues: int = 10) -> Iterator[Issue]:
                return iter([])

            def get_board(self, board_id: str) -> Board:  # type: ignore[empty-body]
                ...

            def get_boards(self) -> Iterator[Board]:
                return iter([])

            def get_lists(self, board_id: str) -> Iterator[List]:
                return iter([])

            def get_members_on_card(self, issue_id: str) -> list[Member]:
                return []

            def assign_issue(self, issue_id: str, member_id: str) -> bool:
                return True

            def create_issue(
                self,
                title: str,
                list_id: str,
                *,
                description: str | None = None,
            ) -> Issue:
                return True

        client = ConcreteClient()
        assert client is not None
        assert isinstance(client, Client)


@pytest.mark.unit
class TestGetClientFactory:
    """Test the get_client factory function."""

    def test_get_client_not_implemented(self) -> None:
        """Test that get_client raises NotImplementedError."""
        with pytest.raises(NotImplementedError, match="Subclasses must implement"):
            get_client()

    def test_get_client_with_interactive_flag(self) -> None:
        """Test that get_client rejects interactive flag when not implemented."""
        with pytest.raises(NotImplementedError, match="Subclasses must implement"):
            get_client(interactive=True)
