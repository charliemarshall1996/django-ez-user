from django.apps import apps
import pytest

from accounts.apps import AccountsConfig


@pytest.fixture
def user_config():
    return {"default_auto_field": "django.db.models.BigAutoField", "name": "accounts"}


@pytest.mark.django_db
def test_user_config(user_config):
    assert user_config["name"] == AccountsConfig.name
    assert user_config["name"] == apps.get_app_config("accounts").name
    assert user_config["default_auto_field"] == AccountsConfig.default_auto_field
    assert (
        user_config["default_auto_field"]
        == apps.get_app_config("accounts").default_auto_field
    )
