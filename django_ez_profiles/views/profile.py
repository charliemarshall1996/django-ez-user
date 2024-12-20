import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
User = get_user_model()


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/profile.html"
    slug_field = "id"
    slug_url_kwarg = "slug"

    def get_object(self):
        """
        Retrieve the current user object.

        This method returns the user object associated with the
        current authenticated session.

        Returns:
            - `User`: The currently authenticated user.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Add the user ID to the context data.

        This method adds the user ID to the context data for
        the view, which is used to render the template.

        Returns:
            - `dict`: The context data with the user ID added.
        """

        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        return context
