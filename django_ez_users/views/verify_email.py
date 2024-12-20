from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect

from django_ez_users.messages import AccountsMessageManager


def verify_email_view(request, user_id, token):
    """
    View that verifies a user's email address.

    Args:
        - request (`django.http.HttpRequest`): The request object.
        - user_id (`int`): The ID of the user to verify.
        - token (`str`): The verification token.

    Returns:
        - A redirect to the login page if the token is valid,
        or a 404 if the user or token is invalid.

    """
    from django_ez_users.tokens import email_verification_token  # Import the token generator

    UserModel = get_user_model()
    user = get_object_or_404(UserModel, id=user_id)

    if email_verification_token.check_token(user, token):
        user.email_verified = True
        user.save()
        messages.success(request, AccountsMessageManager.email_verified)
        return redirect("accounts:login")
