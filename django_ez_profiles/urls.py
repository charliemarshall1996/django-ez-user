from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "accounts"
urlpatterns = [
    path("registration/", views.registration_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/<int:id>/", views.ProfileView.as_view(), name="profile"),
    path("settings/<int:id>/", views.settings_view, name="settings"),
    path("password-reset/", views.password_reset_view, name="password_reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "verify-email/<int:user_id>/<str:token>/",
        views.verify_email_view,
        name="verify_email",
    ),
    path("resend/", views.resend_view, name="resend"),
    path("delete-account/", views.delete_account_view, name="delete_account"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
