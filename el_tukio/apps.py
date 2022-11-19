from django.apps import AppConfig


class ElTukioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'el_tukio'

    def ready(self):
        import el_tukio.signals