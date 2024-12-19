from django.apps import AppConfig


class DarklightConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'darklight'

    def ready(self):
        import darklight.signals