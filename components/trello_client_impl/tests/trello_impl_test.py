"""Unit tests for the Trello client implementation."""

import os

import pytest
from unittest.mock import MagicMock, patch

from trello_client_impl.trello_impl import (
    TrelloCard,
    TrelloBoard,
    TrelloMember,
    TrelloClient,
    get_client_impl,
    register,
)


@pytest.mark.unit
class TestTrelloCard:
    """Test the TrelloCard implementation."""

    def test_trello_card_initialization(self):
        """Test TrelloCard can be initialized with required fields."""
        card = TrelloCard(
            id="card_123",
            title="Test Card",
            isComplete=False,
            dueComplete=False,
            desc="Test description",
            due="2026-02-15",
            idBoard="board_123",
            idList="list_123",
        )
        assert card.id == "card_123"
        assert card.title == "Test Card"
        assert card.isComplete is False
        assert card.dueComplete is False
        assert card.desc == "Test description"
        assert card.due == "2026-02-15"

    def test_trello_card_from_api(self, mock_card_response):
        """Test TrelloCard.from_api static method."""
        card = TrelloCard.from_api(mock_card_response)
        assert card.id == mock_card_response["id"]

    def test_trello_card_properties(self):
        """Test TrelloCard properties are accessible."""
        card = TrelloCard(
            id="test_id",
            title="Test",
            isComplete=True,
            dueComplete=True,
            desc="Test",
            due="2026-02-15",
            idBoard="board_1",
            idList="list_1",
        )
        assert hasattr(card, "id")
        assert hasattr(card, "title")
        assert hasattr(card, "isComplete")
        assert hasattr(card, "dueComplete")
        assert hasattr(card, "desc")


@pytest.mark.unit
class TestTrelloBoard:
    """Test the TrelloBoard implementation."""

    def test_trello_board_initialization(self):
        """Test TrelloBoard can be initialized."""
        board = TrelloBoard(id="board_123", name="Test Board")
        assert board.id == "board_123"
        assert board.name == "Test Board"

    def test_trello_board_from_api(self, mock_board_response):
        """Test TrelloBoard.from_api static method."""
        board = TrelloBoard.from_api(mock_board_response)
        assert board.id == mock_board_response["id"]
        assert board.name == mock_board_response["name"]

    def test_trello_board_properties(self):
        """Test TrelloBoard properties are accessible."""
        board = TrelloBoard(id="test_id", name="Test Board")
        assert hasattr(board, "id")
        assert hasattr(board, "name")
        assert board.id == "test_id"
        assert board.name == "Test Board"


@pytest.mark.unit
class TestTrelloMember:
    """Test the TrelloMember implementation."""

    def test_trello_member_initialization(self):
        """Test TrelloMember can be initialized."""
        member = TrelloMember(
            id="member_123", username="testuser", confirmed=True
        )
        assert member.id == "member_123"
        assert member.username == "testuser"
        assert member.confirmed is True

    def test_trello_member_from_api(self, mock_member_response):
        """Test TrelloMember.from_api static method."""
        member = TrelloMember.from_api(mock_member_response)
        assert member.id == mock_member_response["id"]

    def test_trello_member_optional_fields(self):
        """Test TrelloMember with optional fields."""
        member = TrelloMember(id="member_123", username=None, confirmed=None)
        assert member.id == "member_123"
        assert member.username is None
        assert member.confirmed is None


@pytest.mark.unit
class TestTrelloClient:
    """Test the TrelloClient implementation with mocked requests."""

    @pytest.fixture
    def client_with_env(self, mock_os_environ):
        """Create a TrelloClient with mocked environment."""
        return TrelloClient()

    def test_trello_client_initialization(self, mock_os_environ):
        """Test TrelloClient can be initialized."""
        client = TrelloClient()
        assert client is not None
        assert client.interactive is False

    def test_trello_client_interactive_mode(self, mock_os_environ):
        """Test TrelloClient with interactive flag."""
        client = TrelloClient(interactive=True)
        assert client.interactive is True

    def test_trello_client_api_key_from_env(self, mock_os_environ):
        """Test TrelloClient loads API key from environment."""
        client = TrelloClient()
        assert client.api_key == "test_api_key"

    def test_trello_client_token_property(self, mock_os_environ):
        """Test TrelloClient token property."""
        client = TrelloClient()
        assert client.token == "test_token"

    def test_trello_client_query_method(self, mock_os_environ):
        """Test TrelloClient _query method includes credentials."""
        client = TrelloClient()
        query = client._query()
        assert "key" in query
        assert "token" in query
        assert query["key"] == "test_api_key"
        assert query["token"] == "test_token"

    def test_trello_client_get_issue(self, client_with_env, mocker, mock_card_response):
        """Test TrelloClient.get_issue with mocked API call."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_card_response
        mocker.patch(
            "trello_client_impl.trello_impl.requests.request",
            return_value=mock_response,
        )

        client = TrelloClient()
        client.api_key = "test_key"
        client._token = "test_token"

        issue = client.get_issue("card_id")
        assert issue is not None

    def test_trello_client_delete_issue(self, client_with_env, mocker):
        """Test TrelloClient.delete_issue with mocked API call."""
        mock_response = MagicMock()
        mocker.patch(
            "trello_client_impl.trello_impl.requests.request",
            return_value=mock_response,
        )

        client = TrelloClient()
        client.api_key = "test_key"
        client._token = "test_token"

        result = client.delete_issue("card_id")
        assert result is True

    def test_trello_client_mark_complete(self, client_with_env, mocker):
        """Test TrelloClient.mark_complete with mocked API call."""
        mock_response = MagicMock()
        mocker.patch(
            "trello_client_impl.trello_impl.requests.request",
            return_value=mock_response,
        )

        client = TrelloClient()
        client.api_key = "test_key"
        client._token = "test_token"

        result = client.mark_complete("card_id")
        assert result is True

    def test_trello_client_get_board(self, client_with_env, mocker, mock_board_response):
        """Test TrelloClient.get_board with mocked API call."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_board_response
        mocker.patch(
            "trello_client_impl.trello_impl.requests.request",
            return_value=mock_response,
        )

        client = TrelloClient()
        client.api_key = "test_key"
        client._token = "test_token"

        board = client.get_board("board_id")
        assert board is not None

    def test_trello_client_get_members_on_card(
        self, client_with_env, mocker, mock_member_response
    ):
        """Test TrelloClient.get_members_on_card with mocked API call."""
        mock_response = MagicMock()
        mock_response.json.return_value = [mock_member_response]
        mocker.patch(
            "trello_client_impl.trello_impl.requests.request",
            return_value=mock_response,
        )

        client = TrelloClient()
        client.api_key = "test_key"
        client._token = "test_token"

        members = client.get_members_on_card("card_id")
        assert isinstance(members, list)

    def test_trello_client_get_issues(self, client_with_env, mocker, mock_card_response):
        """Test TrelloClient.get_issues returns an iterator."""
        mock_response = MagicMock()
        mock_response.json.return_value = [mock_card_response]
        mocker.patch(
            "trello_client_impl.trello_impl.requests.request",
            return_value=mock_response,
        )

        client = TrelloClient()
        client.api_key = "test_key"
        client._token = "test_token"
        client._default_board_id = "board_id"

        issues = client.get_issues(max_issues=10)
        assert hasattr(issues, "__iter__")


@pytest.mark.unit
class TestGetClientImpl:
    """Test the get_client_impl factory function."""

    def test_get_client_impl_returns_trello_client(self, mock_os_environ):
        """Test get_client_impl returns a TrelloClient instance."""
        client = get_client_impl()
        assert isinstance(client, TrelloClient)

    def test_get_client_impl_with_interactive_flag(self, mock_os_environ):
        """Test get_client_impl passes interactive flag."""
        client = get_client_impl(interactive=True)
        assert client.interactive is True


@pytest.mark.unit
class TestRegister:
    """Test the register function."""

    def test_register_function_exists(self):
        """Test that register function is callable."""
        assert callable(register)
