from django.contrib.auth import get_user_model
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_create_user(custom_user_data_factory):
    data = custom_user_data_factory(email_verified=False)
    user = User.objects.create_user(**data)
    assert user.email == data["email"]
    assert user.first_name == data["first_name"]
    assert user.last_name == data["last_name"]
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    assert str(user) == data["email"]


@pytest.mark.django_db
def test_create_user_null_email(custom_user_data_factory):
    data = custom_user_data_factory()
    data["email"] = None
    with pytest.raises(ValueError):
        User.objects.create_user(**data)


@pytest.mark.django_db
def test_create_superuser(custom_user_data_factory):
    data = custom_user_data_factory(email_verified=False)
    email = data.pop("email")
    data["is_staff"] = True
    user = User.objects.create_superuser(
        email=email, password=data.pop("password"), **data
    )
    assert user.email == email
    assert user.first_name == data["first_name"]
    assert user.last_name == data["last_name"]
    assert user.is_active
    assert user.is_staff
    assert user.is_superuser
    assert str(user) == email


@pytest.mark.django_db
def test_create_superuser_not_staff(custom_user_data_factory):
    data = custom_user_data_factory(email_verified=False)
    email = data.pop("email")
    data["is_staff"] = False

    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email=email, password=data.pop("password"), **data
        )


@pytest.mark.django_db
def test_create_superuser_not_superuser(custom_user_data_factory):
    data = custom_user_data_factory(email_verified=False)
    email = data.pop("email")
    data["is_superuser"] = False

    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email=email, password=data.pop("password"), **data
        )
