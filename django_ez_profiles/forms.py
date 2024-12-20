from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Profile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ["email", "password1", "password2", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["password1"].required = True
        self.fields["password2"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    def clean_email(self):
        """
        Cleans the email field by validating the email address.

        Raises:
        - forms.ValidationError if the email is invalid.

        Returns:
        - str: the cleaned email address."""
        email = self.cleaned_data.get("email")
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email")
        return email

    def save(self):
        return super().save(commit=False)


class UserUpdateForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]

    def save(self):
        """
        Saves the user with the given data
        without committing to the database.

        Returns:
            User: the saved user
        """
        return super().save(commit=False)


class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["birth_date", "email_comms_opt_in"]

        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }

    def save(self) -> Profile:
        """
        Saves the profile with the given
        data without committing to the database.

        Returns:
            Profile: the saved profile instance
        """

        return super().save(commit=False)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["birth_date", "email_comms_opt_in"]

    def save(self) -> Profile:
        """
        Saves the profile with the given
        data without committing to the database.

        Returns:
            Profile: the saved profile instance
        """
        return super().save(commit=False)


class LoginForm(forms.Form):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class ResendVerificationEmailForm(forms.Form):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    email = forms.EmailField(required=True)


class PasswordResetForm(forms.Form):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    email = forms.EmailField(required=True)
