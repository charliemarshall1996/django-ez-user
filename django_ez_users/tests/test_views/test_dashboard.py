from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_get_dashboard_view(client, profile_factory):
    PASSWORD = "securepassword"
    profile = profile_factory(password=PASSWORD)
    profile.save()
    client.force_login(profile.user)
    url = reverse("accounts:dashboard")

    response = client.get(url)
    assert response.status_code == 200
