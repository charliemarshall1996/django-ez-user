import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from django_ez_users.messages import AccountsMessageManager

User = get_user_model()


@pytest.mark.django_db
def test_profile_settings_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": PASSWORD}
    )

    assert response.status_code == 302

    url = reverse("accounts:settings", kwargs={"id": profile.id})

    # GET request should render the profile settings page
    response = client.get(url)
    assert response.status_code == 200

    assert "user_form" in response.context
    assert "profile_form" in response.context

    # POST request with valid data should update profile
    data = {
        "honeypot": "",
        "email": profile.user.email,
        "first_name": "Updated Name",
        "last_name": "Updated Lastname",
        "daily_target": 100,
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse(
        "accounts:profile", kwargs={"id": profile.id})

    # Check success message
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.profile_update_success


@pytest.mark.django_db
def test_profile_settings_view_invalid_profile(
    client, profile_factory, custom_user_factory
):
    PASSWORD = "securepassword"

    user_profile = profile_factory(password=PASSWORD)
    user_profile.save()
    profile = profile_factory(password=PASSWORD)
    profile.save()

    assert user_profile
    assert profile

    response = client.post(
        reverse("accounts:login"),
        {"email": user_profile.user.email, "password": PASSWORD},
    )

    assert response.status_code == 302
    print(f"Login response {list(get_messages(response.wsgi_request))}")
    print(f"user authenticated: {user_profile.user.is_authenticated}")

    url = reverse("accounts:settings", kwargs={"id": profile.user.profile.id})

    response = client.get(url)
    # assert response.status_code == 302

    # Check success message
    messages = list(get_messages(response.wsgi_request))
    print(messages)
    assert str(
        messages[0]) == "You are not authorized to view or edit this profile."


@pytest.mark.django_db
def test_profile_settings_view_invalid_birth_date(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": PASSWORD}
    )

    assert response.status_code == 302

    url = reverse("accounts:settings", kwargs={"id": profile.id})

    # GET request should render the profile settings page
    response = client.get(url)
    assert response.status_code == 200

    assert "user_form" in response.context
    assert "profile_form" in response.context

    # POST request with valid data should update profile
    data = {
        "honeypot": "",
        "email": profile.user.email,
        "first_name": "Updated Name",
        "last_name": "Updated Lastname",
        "daily_target": 100,
        "birth_date": "invalid-date",
    }

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse(
        "accounts:profile", kwargs={"id": profile.id})

    # Check error message
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.invalid_birth_date


@pytest.mark.django_db
def test_profile_settings_view_invalid_user_form():
    pass


@pytest.mark.django_db
def test_profile_settings_view_invalid_target_form():
    pass
