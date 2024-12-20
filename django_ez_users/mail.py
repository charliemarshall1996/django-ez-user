from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.mail import EmailManager


class AccountsEmailManager(EmailManager):
    def __init__(self):
        super().__init__()

    def mail_verification(self, request, user):
        """
        Sends an email to the user with a verification link to
        confirm their email address.

        Args:
        - `request`: The HTTP request object, used to build the
          absolute URI for the verification link.
        - `user`: The user object for whom the email verification
          link is being generated.

        The email contains a token-based verification URL which
        when clicked will verify the user's email address.
        """
        # Generate verification token
        from .tokens import email_verification_token

        token = email_verification_token.make_token(user)

        # Build verification URL
        verification_url = request.build_absolute_uri(
            reverse(
                "accounts:verify_email", kwargs={"user_id": user.id, "token": token}
            )
        )

        # Send email
        subject = "Verify your email"
        message = f"Please click the link to verify your email: {verification_url}"
        html_message = (
            f"<p>Please click the link to verify your email: {verification_url}</p>"
        )
        recipient = [user.email]
        self.send(subject, message, html_message, recipient)

    def mail_password_reset(self, request, user):
        """
        Sends an email to the user with a password reset link.

        Args:
        - `request`: The HTTP request object, used to build the
        absolute URI for the password reset link.
        - `user`: The user object for whom the password reset
        link is being generated.

        The email contains a token-based password reset URL
        which, when clicked, allows the user to reset their
        password.
        """
        # Generate password reset token
        from .tokens import password_reset_token

        token = password_reset_token.make_token(user)

        # Build password reset URL
        password_reset_url = request.build_absolute_uri(
            reverse(
                "accounts:password_reset_confirm",
                kwargs={
                    "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": token,
                },
            )
        )

        # Send email
        subject = "Reset your password"
        message = f"Please click the link to reset your password: {password_reset_url}"
        html_message = (
            f"<p>Please click the link to reset your password: {password_reset_url}</p>"
        )
        recipient = [user.email]
        self.send(subject, message, html_message, recipient)
