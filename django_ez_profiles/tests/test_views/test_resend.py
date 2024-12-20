from datetime import timedelta
from unittest.mock import Mock, patch

import pytest
from django.urls import reverse
from django.contrib.messages import get_messages

from django_ez_users.messages import AccountsMessageManager


@pytest.mark.django_db
def test_resend(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": PASSWORD}
    )

    assert response.status_code == 302
    url = reverse("accounts:resend")

    # GET request should render the resend form
    response = client.get(url)
    assert response.status_code == 200

    assert "form" in response.context

    # POST with valid email should resend the email
    data = {"honeypot": "", "email": profile.user.email}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse("accounts:login")
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "A verification email has been sent."


@pytest.mark.django_db
def test_resend_spam(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": PASSWORD}
    )

    assert response.status_code == 302
    url = reverse("accounts:resend")

    # GET request should render the resend form
    response = client.get(url)
    assert response.status_code == 200

    assert "form" in response.context

    # POST with valid email should resend the email
    data = {"honeypot": "spam", "email": profile.user.email}

    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect after spam
    assert response.url == reverse("core:home")
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.spam


@pytest.mark.django_db
def test_resend_email_not_found(client, profile_factory):
    # Create profile and user
    PASSWORD = "securepassword"
    profile = profile_factory(password=PASSWORD)
    profile.save()

    # Login
    client.force_login(profile.user)

    # Get the password reset page
    url = reverse("accounts:resend")
    response = client.get(url)

    # Post data with a non-existent email
    data = {"honeypot": "", "email": "a@b.com"}
    response = client.post(url, data)

    # Response should redirect
    # to the password reset page
    assert response.status_code == 302
    assert response.url == reverse("accounts:resend")

    # Response should display an
    # email not found error message
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.email_not_found


@pytest.mark.django_db
def test_resend_email_cannot_resend(client, profile_factory):
    # Create profile and user
    PASSWORD = "securepassword"
    profile = profile_factory(password=PASSWORD)
    profile.save()

    # Login
    client.force_login(profile.user)

    # Mock get_time_since_last_email to return 0
    # (less than timeout value of 10)
    mock_get_time_since_last_email = Mock(return_value=timedelta(minutes=0))
    with patch(
        "accounts.views.resend.get_time_since_last_email",
        mock_get_time_since_last_email,
    ):
        url = reverse("accounts:resend")
        response = client.post(
            url, {"honeypot": "", "email": profile.user.email})

    # Response should redirect
    # to the resend page
    assert response.status_code == 302
    assert response.url == reverse("accounts:resend")

    # Response should display an
    # info message to wait before
    # resending
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.resend_email_wait(
        float(10.0))
