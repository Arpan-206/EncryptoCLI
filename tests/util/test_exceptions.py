"""Tests for custom exceptions."""

import pytest

from encryptocli.util.exceptions import FatalError, MildError


class TestExceptions:
    """Test custom exception classes."""

    def test_fatal_error_default_message(self):
        """Test FatalError with default message."""
        error = FatalError()
        assert str(error) == "Fatal Error"

    def test_fatal_error_custom_message(self):
        """Test FatalError with custom message."""
        error = FatalError("Custom fatal error")
        assert str(error) == "Custom fatal error"

    def test_fatal_error_is_exception(self):
        """Test that FatalError is an Exception."""
        error = FatalError()
        assert isinstance(error, Exception)

    def test_fatal_error_can_be_raised(self):
        """Test that FatalError can be raised and caught."""
        with pytest.raises(FatalError):
            raise FatalError("Test error")

    def test_mild_error_default_message(self):
        """Test MildError with default message."""
        error = MildError()
        assert str(error) == "Mild Error"

    def test_mild_error_custom_message(self):
        """Test MildError with custom message."""
        error = MildError("Custom mild error")
        assert str(error) == "Custom mild error"

    def test_mild_error_is_exception(self):
        """Test that MildError is an Exception."""
        error = MildError()
        assert isinstance(error, Exception)

    def test_mild_error_can_be_raised(self):
        """Test that MildError can be raised and caught."""
        with pytest.raises(MildError):
            raise MildError("Test error")
