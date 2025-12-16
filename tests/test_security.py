"""Tests for security functions."""
import pytest
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token,
)


class TestPasswordHashing:
    """Tests for password hashing."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "TestPassword123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password_correct(self):
        """Test verifying correct password."""
        password = "TestPassword123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verifying incorrect password."""
        password = "TestPassword123"
        hashed = get_password_hash(password)
        assert verify_password("WrongPassword", hashed) is False


class TestJWT:
    """Tests for JWT tokens."""

    def test_create_and_decode_token(self):
        """Test creating and decoding JWT token."""
        data = {"sub": "123", "email": "test@example.com", "plan": "free"}
        token = create_access_token(data)
        assert token is not None
        assert len(token) > 0

        decoded = decode_token(token)
        assert decoded is not None
        assert decoded["sub"] == "123"
        assert decoded["email"] == "test@example.com"

    def test_decode_invalid_token(self):
        """Test decoding invalid token."""
        invalid_token = "invalid.token.here"
        decoded = decode_token(invalid_token)
        assert decoded is None



