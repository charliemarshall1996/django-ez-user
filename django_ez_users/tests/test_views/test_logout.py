import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_logout_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {"email": profile.user.email, "password": PASSWORD}
    )

    assert response.status_code == 302
    url = reverse("accounts:logout")

    # Logout and ensure redirection to home
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse("core:home")
