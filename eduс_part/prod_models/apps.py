from django.apps import AppConfig


class ProdModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prod_models'

    def ready(self):
        import prod_models.signals

