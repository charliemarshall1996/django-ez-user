from django.contrib.auth import authenticate
import pytest


@pytest.mark.django_db
def test_authenticate_verified_user(custom_user_factory):
    """Test that an email-verified user can authenticate."""
    PASSWORD = "securepassword"
    verified_user = custom_user_factory(password=PASSWORD)
    user = authenticate(email=verified_user.email, password=PASSWORD)
    assert user is not None
    assert user.email == verified_user.email


@pytest.mark.django_db
def test_authenticate_unverified_user(custom_user_factory):
    """Test that an unverified user cannot authenticate."""
    PASSWORD = "securepassword"
    verified_user = custom_user_factory(password=PASSWORD, email_verified=False)
    user = authenticate(email=verified_user.email, password=PASSWORD)
    assert user is None


@pytest.mark.django_db
def test_authenticate_non_existent_user():
    """Test that a non-existent user cannot authenticate."""
    user = authenticate(email="nonexistent@example.com", password="securepassword")
    assert user is None


@pytest.mark.django_db
def test_authenticate_invalid_password(custom_user_factory):
    """Test that an invalid password cannot authenticate."""
    PASSWORD = "securepassword"
    user = custom_user_factory(password=PASSWORD)
    user = authenticate(email=user.email, password="wrongpassword")
    assert user is None
