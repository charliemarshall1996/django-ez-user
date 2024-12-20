import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from django_ez_users.messages import AccountsMessageManager

User = get_user_model()


@pytest.mark.django_db
def test_register_view_valid(client, user_registration_form_data):
    email = user_registration_form_data["email"]

    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200

    url = reverse("accounts:register")

    # GET request should render the register form
    response = client.post(url, user_registration_form_data)
    user = User.objects.get(email=email)
    assert response.status_code == 302
    assert response.url == reverse("accounts:login")
    assert user
    assert user.profile


@pytest.mark.django_db
def test_register_view_invalid_email(client, user_registration_form_data):
    user_registration_form_data["email"] = "invalid_email"

    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200

    url = reverse("accounts:register")

    # GET request should render the register form
    response = client.post(url, user_registration_form_data)
    assert response.status_code == 302
    assert response.url == reverse("accounts:register")

    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Please enter a valid email address."


@pytest.mark.django_db
def test_register_view_spam(client, user_registration_form_data):
    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200
    user_registration_form_data["honeypot"] = "spam"
    url = reverse("accounts:register")

    # GET request should render the register form
    response = client.post(url, user_registration_form_data)
    assert response.status_code == 302
    assert response.url == reverse("core:home")

    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.spam


@pytest.mark.django_db
def test_register_view_mismatched_password(client, user_registration_form_data):
    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200
    user_registration_form_data["password2"] = "incorrect_password"
    url = reverse("accounts:register")

    # GET request should render the register form
    response = client.post(url, user_registration_form_data)
    assert response.status_code == 302
    assert response.url == reverse("accounts:register")

    messages = list(get_messages(response.wsgi_request))
    print(str(messages[0]))
    assert str(messages[0]) == "Please enter a valid password."


@pytest.mark.django_db
def test_register_view_password_too_common(client, user_registration_form_data):
    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200
    user_registration_form_data["password1"] = "password1"
    user_registration_form_data["password2"] = "password1"
    url = reverse("accounts:register")

    # GET request should render the register form
    response = client.post(url, user_registration_form_data)
    assert response.status_code == 302
    assert response.url == reverse("accounts:register")

    messages = list(get_messages(response.wsgi_request))
    print(str(messages[0]))
    assert str(messages[0]) == "Please enter a valid password."
