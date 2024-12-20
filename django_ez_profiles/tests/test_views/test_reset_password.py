import pytest
from django.urls import reverse
from django.contrib.messages import get_messages

from django_ez_users.messages import AccountsMessageManager


@pytest.mark.django_db
def test_password_reset_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": PASSWORD}
    )

    assert response.status_code == 302
    url = reverse("accounts:password_reset")

    # GET request should render the password reset form
    response = client.get(url)
    assert response.status_code == 200

    assert "form" in response.context

    # POST with a valid email should send a password reset email
    data = {"honeypot": "", "email": profile.user.email}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.password_reset_success


@pytest.mark.django_db
def test_password_reset_view_spam(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": PASSWORD}
    )

    assert response.status_code == 302
    url = reverse("accounts:password_reset")

    # GET request should render the password reset form
    response = client.get(url)
    assert response.status_code == 200

    assert "form" in response.context

    # Test honeypot field for spam
    data = {"honeypot": "spam", "email": profile.user.email}
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect after spam
    assert response.url == reverse("core:home")
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.spam


@pytest.mark.django_db
def test_password_reset_view_email_does_not_exist(client, profile_factory):
    # Create user and profile
    PASSWORD = "securepassword"
    profile = profile_factory(password=PASSWORD)
    profile.save()

    # Login
    client.force_login(profile.user)

    # Get the password reset page
    url = reverse("accounts:password_reset")
    response = client.get(url)

    # Post data with a non-existent email
    data = {"honeypot": "", "email": "a@b.com"}
    response = client.post(url, data)

    # Response should redirect
    # to the password reset page
    assert response.status_code == 302
    assert response.url == reverse("accounts:password_reset")

    # Response should display an
    # email not found error message
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.email_not_found
