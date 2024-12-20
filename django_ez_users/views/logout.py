import logging

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@login_required
def logout_view(request):
    """
    Log out the user and redirect to the home page.

    This view logs out the currently authenticated user and
    redirects them to the home page. It requires the user to
    be logged in before accessing it.

    Args:
        request: The HTTP request object.

    Returns:
        A redirect to the home page.
    """

    logout(request)
    return redirect("core:home")
