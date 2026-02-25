"""Conftest for issue_tracker_client_api tests."""

import pytest


@pytest.fixture
def sample_board_data() -> dict:
    """Provide sample board data for testing."""
    return {"id": "board_id_1", "name": "Sample Board"}


@pytest.fixture
def sample_issue_data() -> dict:
    """Provide sample issue/card data for testing."""
    return {
        "id": "card_id_1",
        "title": "Sample Issue",
        "isComplete": False,
    }


@pytest.fixture
def sample_member_data() -> dict:
    """Provide sample member data for testing."""
    return {
        "id": "member_id_1",
        "username": "sample_user",
        "confirmed": True,
    }
