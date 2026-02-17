"""Unit tests for the Member abstract class."""

from abc import ABC

import pytest
from issue_tracker_client_api.member import Member, get_member


@pytest.mark.unit
class TestMemberAbstractClass:
    """Test that Member is an abstract base class with required properties."""

    def test_member_is_abstract(self):
        """Test that Member cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            _ = Member()  # type: ignore

    def test_member_is_abc(self):
        """Test that Member is an ABC."""
        assert issubclass(Member, ABC)

    def test_member_has_id_property(self):
        """Test that Member has an id property."""
        assert hasattr(Member, "id")
        assert isinstance(Member.id, property)

    def test_member_has_username_property(self):
        """Test that Member has a username property."""
        assert hasattr(Member, "username")
        assert isinstance(Member.username, property)

    def test_member_has_confirmed_property(self):
        """Test that Member has a confirmed property."""
        assert hasattr(Member, "confirmed")
        assert isinstance(Member.confirmed, property)

    def test_concrete_member_implementation(self, sample_member_data):
        """Test a concrete Member implementation."""

        class ConcreteMember(Member):
            """Concrete implementation of Member for testing."""

            def __init__(self, id: str, username: str | None, confirmed: bool | None):
                self._id = id
                self._username = username
                self._confirmed = confirmed

            @property
            def id(self) -> str:
                return self._id

            @property
            def username(self) -> str | None:
                return self._username

            @property
            def confirmed(self) -> bool | None:
                return self._confirmed

        member = ConcreteMember(
            id=sample_member_data["id"],
            username=sample_member_data["username"],
            confirmed=sample_member_data["confirmed"],
        )
        assert member.id == sample_member_data["id"]
        assert member.username == sample_member_data["username"]
        assert member.confirmed == sample_member_data["confirmed"]

    def test_member_with_none_properties(self):
        """Test that Member properties can be None."""

        class ConcreteMember(Member):
            """Concrete implementation of Member for testing."""

            def __init__(self, id: str):
                self._id = id

            @property
            def id(self) -> str:
                return self._id

            @property
            def username(self) -> str | None:
                return None

            @property
            def confirmed(self) -> bool | None:
                return None

        member = ConcreteMember(id="test_id")
        assert member.id == "test_id"
        assert member.username is None
        assert member.confirmed is None


@pytest.mark.unit
class TestGetMemberFactory:
    """Test the get_member factory function."""

    def test_get_member_not_implemented(self):
        """Test that get_member raises NotImplementedError."""
        with pytest.raises(NotImplementedError, match="Subclasses must implement"):
            get_member("test_member_id")
