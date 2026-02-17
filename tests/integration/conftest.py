"""Conftest for integration tests."""

from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_requests_integration(mocker):
    """Provide a mock requests module for integration tests."""
    return mocker.patch("requests.request")


@pytest.fixture
def integration_env_setup(mocker):
    """Setup environment for integration tests with mocked credentials."""
    return mocker.patch.dict(
        "os.environ",
        {
            "TRELLO_API_KEY": "integration_test_api_key",
            "TRELLO_TOKEN": "integration_test_token",
            "TRELLO_BOARD_ID": "integration_test_board_id",
        },
    )


@pytest.fixture
def mock_client_implementation():
    """Provide a mock client implementation for integration tests."""
    mock_client = MagicMock()
    mock_client.get_issue = MagicMock()
    mock_client.delete_issue = MagicMock(return_value=True)
    mock_client.mark_complete = MagicMock(return_value=True)
    mock_client.get_issues = MagicMock()
    mock_client.get_board = MagicMock()
    mock_client.get_members_on_card = MagicMock()
    return mock_client


@pytest.fixture
def mock_card_response() -> dict:
    """Provide a mock Trello card API response for integration tests."""
    return {
        "id": "test_card_id",
        "name": "Test Card",
        "desc": "Test card description",
        "dueComplete": False,
        "due": "2026-02-15T23:59:59.000Z",
        "idBoard": "test_board_id",
        "idList": "test_list_id",
    }


@pytest.fixture
def mock_board_response() -> dict:
    """Provide a mock Trello board API response for integration tests."""
    return {
        "id": "test_board_id",
        "name": "Test Board",
    }


@pytest.fixture
def mock_member_response() -> dict:
    """Provide a mock Trello member API response for integration tests."""
    return {
        "id": "test_member_id",
        "username": "testuser",
        "fullName": "Test User",
        "initials": "TU",
        "confirmed": True,
    }
