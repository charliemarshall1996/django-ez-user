import pytest
from django.urls import reverse
from django.contrib.messages import get_messages

from django_ez_users.messages import AccountsMessageManager


@pytest.mark.django_db
def test_delete_account_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {
            "email": profile.user.email, "password": PASSWORD}
    )

    assert response.status_code == 302
    url = reverse("accounts:delete_account")

    print(f"URL: {url}")
    # GET request should render the delete confirmation page
    response = client.get(url)
    assert response.status_code == 200

    # POST request should delete the account
    response = client.post(url)
    assert response.status_code == 302  # Should redirect
    assert response.url == reverse("core:home")
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == AccountsMessageManager.account_deleted_success
