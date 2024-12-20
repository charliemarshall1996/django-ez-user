from django.contrib import admin
from django.apps import apps

# Get all models from the 'core' app
app_models = apps.get_app_config("accounts").get_models()

for model in app_models:
    if model not in admin.site._registry:
        admin.site.register(model)
