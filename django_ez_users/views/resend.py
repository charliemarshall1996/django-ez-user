from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.utils import timezone

from django_ez_users.forms import ResendVerificationEmailForm
from django_ez_users.mail import AccountsEmailManager
from django_ez_users.messages import AccountsMessageManager

from .utils import get_time_since_last_email, get_minutes_left_before_resend

User = get_user_model()

email_manager = AccountsEmailManager()


def resend_view(request):
    """
    A view that handles the resend verification email form submission.

    If the form is valid, it sends a verification email to the user and
    redirects to the login page. If the form is invalid, it redirects to
    the home page with an error message.

    Args:
        - request (`django.http.HttpRequest`): The request object.

    Returns:
        - `django.http.HttpResponse`: The response object.
    """
    if request.method == "POST":
        form = ResendVerificationEmailForm(request.POST)

        if form.is_valid():
            if form.cleaned_data["honeypot"]:
                messages.error(request, AccountsMessageManager.spam)

                return redirect("core:home")
            email = form.cleaned_data["email"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, AccountsMessageManager.email_not_found)
                return redirect("accounts:resend")

            timeout_duration = timedelta(minutes=10)

            if user.last_verification_email_sent:
                # Calculate the time difference between the current time and
                # the last time the verification email was sent
                time_since_last_email = get_time_since_last_email(
                    user.last_verification_email_sent
                )

                # Calculate the time difference between the timeout duration
                # and the time since the last verification email was sent
                minutes_difference = get_minutes_left_before_resend(
                    time_since_last_email, timeout_duration
                )

                # If the time difference is less than the timeout duration,
                # show an info message to the user to wait
                if time_since_last_email < timeout_duration:
                    messages.info(
                        request,
                        AccountsMessageManager.resend_email_wait(
                            minutes_difference),
                    )
                    return redirect("accounts:resend")

            # Send the verification email and save the last verification email
            # sent time
            email_manager.mail_verification(request, user)
            user.last_verification_email_sent = timezone.now()
            user.save()

            messages.success(
                request, AccountsMessageManager.email_verification_sent)
            return redirect("accounts:login")
    else:
        form = ResendVerificationEmailForm()

    return render(request, "accounts/resend.html", {"form": form})
