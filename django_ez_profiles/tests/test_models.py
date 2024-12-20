import pytest

from django_ez_users.models import CustomUser, Profile


@pytest.mark.django_db
def test_custom_user(custom_user_data_factory):
    data = custom_user_data_factory()
    model = CustomUser(**data)
    assert model.email == data["email"]
    assert model.email_verified == data["email_verified"]
    assert model.last_verification_email_sent == data["last_verification_email_sent"]
    assert model.first_name == data["first_name"]
    assert model.last_name == data["last_name"]
    assert model.is_active == data["is_active"]
    assert model.is_staff == data["is_staff"]
    assert model.date_joined == data["date_joined"]
    assert str(model) == data["email"]


@pytest.mark.django_db
def test_profile(custom_user_factory, profile_data_factory):
    user = custom_user_factory()
    data = profile_data_factory(user)
    model = Profile(**data)
    assert model.user == data["user"]
    assert model.email_comms_opt_in == data["email_comms_opt_in"]
    assert model.birth_date == data["birth_date"]
    assert str(model) == user.email
