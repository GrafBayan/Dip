from django.apps import AppConfig

class MySiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MySite'

    def ready(self):
        import MySite.signals