"""Tests for authentication."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAuth:
    """Tests for authentication endpoints."""

    def test_register_user(self):
        """Test user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "TestPassword123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["email"] == "test@example.com"
        assert data["subscription_plan"] == "free"

    def test_register_duplicate_email(self):
        """Test registering with duplicate email."""
        # First registration
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "TestPassword123",
            },
        )

        # Second registration with same email
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "TestPassword123",
            },
        )
        assert response.status_code == 400

    def test_login_valid_credentials(self):
        """Test login with valid credentials."""
        # First register
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "login@example.com",
                "password": "TestPassword123",
            },
        )

        # Then login
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "login@example.com",
                "password": "TestPassword123",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "user" in data

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "WrongPassword",
            },
        )
        assert response.status_code == 401



