"""Conftest for end-to-end tests.

Note: E2E tests should be configured to run against actual Trello API or a test instance.
For development, these may be skipped if credentials are not available.
"""

import os

import pytest


@pytest.fixture
def e2e_skip_if_no_credentials():
    """Skip e2e tests if Trello credentials are not available."""
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")
    board_id = os.getenv("TRELLO_BOARD_ID")

    if not all([api_key, token, board_id]):
        pytest.skip(
            "Skipping e2e tests: TRELLO_API_KEY, TRELLO_TOKEN, and TRELLO_BOARD_ID required"
        )


@pytest.fixture
def e2e_client_config():
    """Provide e2e test client configuration from environment."""
    return {
        "api_key": os.getenv("TRELLO_API_KEY", ""),
        "token": os.getenv("TRELLO_TOKEN", ""),
        "board_id": os.getenv("TRELLO_BOARD_ID", ""),
    }
