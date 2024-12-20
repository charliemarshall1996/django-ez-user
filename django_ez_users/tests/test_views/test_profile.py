import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_profile_view(client, profile_factory):
    PASSWORD = "securepassword"

    profile = profile_factory(password=PASSWORD)
    profile.save()

    response = client.post(
        reverse("accounts:login"), {"email": profile.user.email, "password": PASSWORD}
    )

    assert response.status_code == 302
    url = reverse("accounts:profile", kwargs={"id": profile.user.profile.id})

    # GET request should show profile details
    response = client.get(url)
    assert response.status_code == 200

    assert response.context["object"] == profile.user
