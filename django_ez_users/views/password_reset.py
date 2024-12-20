from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from django_ez_users.forms import PasswordResetForm
from django_ez_users.mail import AccountsEmailManager
from django_ez_users.messages import AccountsMessageManager

User = get_user_model()

email_manager = AccountsEmailManager()


def password_reset_view(request):
    """
    A view that handles the password reset form submission.

    This view verifies the form and sends an email to the user with a
    password reset link. If the form is invalid, it redirects to the
    home page with an error message.

    Args:
        - request (`django.http.HttpRequest`): The request object.

    Returns:
        - `django.http.HttpResponse`: The response object.
    """
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Check if the honeypot field is filled
            if form.cleaned_data["honeypot"]:
                messages.error(request, AccountsMessageManager.spam)
                return redirect("core:home")

            # Retrieve the email from the form
            email = form.cleaned_data["email"]

            # Check if the user exists
            user = User.objects.filter(email=email).first()
            if user:
                # Send the password reset email
                email_manager.mail_password_reset(request, user)
                messages.success(
                    request, AccountsMessageManager.password_reset_success)
                return redirect("accounts:password_reset")
            else:
                # If the user does not exist, show an error message
                messages.error(request, AccountsMessageManager.email_not_found)
            return redirect("accounts:password_reset")
    else:
        # If the request is GET,
        # create an empty form
        form = PasswordResetForm()
    return render(request, "accounts/password_reset.html", {"form": form})
