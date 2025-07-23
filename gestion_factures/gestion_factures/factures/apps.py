from django.apps import AppConfig

class FacturesConfig(AppConfig):
    """Configuration de l'application factures"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'factures'
    
    def ready(self):
        """Import des signaux au démarrage de l'app"""
        import factures.middleware  # Active les signaux d'historique
