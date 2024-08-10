from django.apps import AppConfig

from users.signals import register_user_signals


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        register_user_signals()
