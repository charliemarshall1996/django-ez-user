from unittest.mock import Mock, patch

import pytest
from django.urls import reverse
from django.contrib.messages import get_messages

from django_ez_users.messages import AccountsMessageManager


@pytest.mark.django_db
def test_login_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    url = reverse("accounts:login")

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert "form" in response.context

    # POST with valid data should log in and redirect
    data = {"honeypot": "", "email": profile.user.email, "password": PASSWORD}
    response = client.post(url, data)
    assert response.status_code == 302
    # Assuming this is the redirect
    assert response.url == reverse("accounts:dashboard")


@pytest.mark.django_db
def test_login_view_invalid_credentials(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    url = reverse("accounts:login")

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert "form" in response.context

    # POST with invalid credentials should show error
    data = {"honeypot": "", "email": profile.user.email,
            "password": "wrongpassword"}
    response = client.post(url, data)
    # assert response.status_code == 302
    assert response.url == reverse("accounts:login")
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.email_not_verified


@pytest.mark.django_db
def test_login_view_spam(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    url = reverse("accounts:login")

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert "form" in response.context

    # Test honeypot field for spam
    data = {
        "honeypot": "spam",
        "email": profile.user.email,
        "password": "securepassword",
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse("core:home")
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.spam


@pytest.mark.django_db
def test_login_view_email_does_not_exist(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    url = reverse("accounts:login")

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert "form" in response.context

    # Test honeypot field for spam
    data = {"honeypot": "", "email": "a@b.com", "password": PASSWORD}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse("accounts:login")
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.email_not_found


@pytest.mark.django_db
def test_login_view_invalid_form(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    url = reverse("accounts:login")

    # GET request should render the login page
    response = client.get(url)
    assert response.status_code == 200

    assert "form" in response.context

    # Test honeypot field for spam
    data = {"honeypot": "", "email": "a@b.c", "password": PASSWORD}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse("accounts:login")
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Login form is not valid"


@pytest.mark.django_db
def test_login_view_non_verified(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD, email_verified=False)
    profile.save()

    url = reverse("accounts:login")

    # GET request should render the login page
    response = client.get(url)

    # Test honeypot field for spam
    data = {"honeypot": "", "email": profile.user.email, "password": PASSWORD}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse("accounts:login")
    messages = list(get_messages(response.wsgi_request))
    url = reverse("accounts:resend")
    assert str(
        messages[0]) == AccountsMessageManager.resend_verification_email(url)


@pytest.mark.django_db
def test_login_view_non_verified_wait(client, profile_factory):
    minutes_left = 1
    mock_can_resend = Mock(return_value=False)
    mock_minutes_left = Mock(return_value=minutes_left)

    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD, email_verified=False)
    profile.save()

    # Get login page
    url = reverse("accounts:login")
    response = client.get(url)

    # post to login page
    data = {"honeypot": "", "email": profile.user.email, "password": PASSWORD}

    with (
        patch("accounts.views.login.get_can_resend", mock_can_resend),
        patch("accounts.views.login.get_minutes_left_before_resend",
              mock_minutes_left),
    ):
        response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse("accounts:login")
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.resend_email_wait(
        minutes_left)


@pytest.mark.django_db
def test_login_view_non_verified_no_last_sent(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(
        password=PASSWORD, email_verified=False, verification_email_sent=False
    )
    profile.save()

    assert not profile.user.last_verification_email_sent

    url = reverse("accounts:login")

    # GET request should render the login page
    response = client.get(url)

    # Test honeypot field for spam
    data = {"honeypot": "", "email": profile.user.email, "password": PASSWORD}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse("accounts:login")
    messages = list(get_messages(response.wsgi_request))
    url = reverse("accounts:resend")
    assert str(
        messages[0]) == AccountsMessageManager.resend_verification_email(url)
