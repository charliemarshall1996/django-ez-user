import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from django_ez_users.tokens import email_verification_token

User = get_user_model()


@pytest.mark.django_db
def test_email_verification_view(client, custom_user_factory):
    user = custom_user_factory(email_verified=False)
    token = email_verification_token.make_token(user)

    url = reverse("accounts:verify_email", kwargs={
                  "user_id": user.id, "token": token})
    response = client.get(url)
    user = User.objects.get(id=user.id)
    assert response.status_code == 302
    assert response.url == reverse("accounts:login")
    assert user.email_verified
