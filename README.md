============
django-ez-user
============

django-ez-user is a Django app to make the addition of custom users and profiles easy.

Detailed documentation is in the "docs" directory.

## Quick start

1. Add "polls" to your INSTALLED_APPS setting like this::

   INSTALLED_APPS = [
   ...,
   "django_ez_users",
   "django_ez_profiles",
   ]

2. Include the polls URLconf in your project urls.py like this::

   [...,
   path("user/", include("django_ez_users.urls")),
   path("profile/", include("django_ez_profiles.urls")),
   ...]

3. Run `python manage.py migrate` to create the models.
