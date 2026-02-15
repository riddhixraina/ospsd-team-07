"""Conftest for trello_client_impl tests."""

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_requests(mocker):
    """Provide a mock requests module."""
    return mocker.patch("trello_client_impl.trello_impl.requests")


@pytest.fixture
def mock_os_environ(mocker):
    """Provide mocked os.environ."""
    return mocker.patch.dict(
        "os.environ",
        {
            "TRELLO_API_KEY": "test_api_key",
            "TRELLO_TOKEN": "test_token",
            "TRELLO_BOARD_ID": "test_board_id",
        },
    )


@pytest.fixture
def trello_client_data():
    """Provide fixture data for Trello client testing."""
    return {
        "api_key": "test_api_key",
        "token": "test_token",
        "board_id": "test_board_id",
        "card_id": "test_card_id",
        "board_name": "Test Board",
        "card_title": "Test Card",
    }


@pytest.fixture
def mock_card_response():
    """Provide a mock Trello card API response."""
    return {
        "id": "test_card_id",
        "name": "Test Card",
        "desc": "Test card description",
        "dueComplete": False,
        "due": "2024-12-31T23:59:59.000Z",
        "idBoard": "test_board_id",
        "idList": "test_list_id",
    }


@pytest.fixture
def mock_board_response():
    """Provide a mock Trello board API response."""
    return {
        "id": "test_board_id",
        "name": "Test Board",
    }


@pytest.fixture
def mock_member_response():
    """Provide a mock Trello member API response."""
    return {
        "id": "test_member_id",
        "username": "testuser",
        "fullName": "Test User",
        "initials": "TU",
        "confirmed": True,
    }
