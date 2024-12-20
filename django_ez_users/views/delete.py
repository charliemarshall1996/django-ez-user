from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from django_ez_users.messages import AccountsMessageManager


@login_required
def delete_account_view(request):
    """Delete a user account

    This view is used to delete a user account. If the request
    method is POST, it deletes the user and their associated
    profile.

    If the request method is GET, it renders a confirmation page
    asking the user whether they want to delete their account.

    Args:
        - request: The HTTP request object

    Returns:
        - A redirect to the home page if the request method is POST
        - A confirmation page if the request method is GET
    """

    if request.method == "POST":
        user = request.user
        user.profile.delete()
        user.delete()
        messages.success(
            request, AccountsMessageManager.account_deleted_success)
        return redirect("core:home")

    # Render the confirmation page
    return render(request, "accounts/delete_account.html")
