import logging

from django.contrib import messages
from django.shortcuts import render, redirect

from django_ez_users.forms import UserRegistrationForm, ProfileRegistrationForm
from django_ez_users.mail import AccountsEmailManager
from django_ez_users.messages import AccountsMessageManager

logger = logging.getLogger(__name__)

email_manager = AccountsEmailManager()


def registration_view(request):
    """
    A view that handles the user registration form submission.

    This view validates the form and sends a verification email
    to the user if the form is valid. If the form is invalid, it
    redirects to the registration page with an error message. If
    the request is GET, it creates an empty form and renders the
    registration page.

    Args:
        - request (`django.http.HttpRequest`): The request object.

    Returns:
        - `django.http.HttpResponse`: The response object.
    """
    if request.method == "POST":
        # Validate the form
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Check if the honeypot field is filled
            if user_form.cleaned_data["honeypot"]:
                messages.error(request, AccountsMessageManager.spam)
                return redirect("core:home")

            # Save the user and profile
            user = user_form.save()
            user.email_verified = False
            user.save()
            profile = profile_form.save()
            profile.user = user
            profile.save()

            # Send verification email
            email_manager.mail_verification(request, user)

            messages.success(
                request,
                "Your account has been created.\nPlease check your email to verify your account.",
            )
            return redirect("accounts:login")

        else:
            # If the form is invalid,
            # show error messages
            if user_form.errors:
                error_data = user_form.errors.as_data()
                email_error = error_data.get("email")
                password_error = error_data.get("password2") or error_data.get(
                    "password1"
                )
                logger.info("User form errors: %s", error_data)
                if email_error:
                    logger.info("Email address is invalid")
                    messages.error(
                        request, AccountsMessageManager.invalid_email)
                if password_error:
                    messages.error(
                        request, AccountsMessageManager.invalid_password)

            return redirect("accounts:register")

    else:
        # If the request is GET, create an empty form
        user_form = UserRegistrationForm()
        profile_form = ProfileRegistrationForm()
    return render(
        request,
        "accounts/register.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
