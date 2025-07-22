from django.apps import AppConfig

class FacturesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'factures'
    
    """ Ici j'importe le middleware """
    def ready(self):
        import factures.middleware
