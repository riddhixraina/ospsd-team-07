"""Root conftest.py for test configuration and shared fixtures."""

import pytest


@pytest.fixture
def mock_trello_api_key() -> str:
    """Provide a mock Trello API key for testing."""
    return "test_api_key_12345"


@pytest.fixture
def mock_trello_token() -> str:
    """Provide a mock Trello token for testing."""
    return "test_token_67890"


@pytest.fixture
def mock_board_id() -> str:
    """Provide a mock board ID for testing."""
    return "mock_board_id_123"


@pytest.fixture
def mock_card_data() -> dict:
    """Provide mock Trello card data."""
    return {
        "id": "mock_card_id",
        "name": "Test Card",
        "desc": "This is a test card",
        "dueComplete": False,
        "due": "2024-12-31T23:59:59.000Z",
        "idBoard": "mock_board_id_123",
        "idList": "mock_list_id_456",
    }


@pytest.fixture
def mock_board_data() -> dict:
    """Provide mock Trello board data."""
    return {
        "id": "mock_board_id_123",
        "name": "Test Board",
        "desc": "A test board",
    }


@pytest.fixture
def mock_member_data() -> dict:
    """Provide mock Trello member data."""
    return {
        "id": "mock_member_id_789",
        "username": "testuser",
        "fullName": "Test User",
        "initials": "TU",
        "avatarUrl": "https://example.com/avatar.jpg",
        "confirmed": True,
    }


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test (fast, isolated)"
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test (medium speed, real dependencies)",
    )
    config.addinivalue_line(
        "markers",
        "e2e: mark test as an end-to-end test (slow, full system)",
    )
