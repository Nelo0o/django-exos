from django.contrib import admin
from .models import Facture, Categorie, HistoriqueFacture

# Actions personnalisées pour la gestion en lot
@admin.action(description="Marquer comme payé")
def marquer_comme_paye(modeladmin, request, queryset):
    """Marque plusieurs factures comme payées en une fois"""
    queryset.update(payee=True)

@admin.action(description="Marquer comme non payé")
def marquer_comme_non_paye(modeladmin, request, queryset):
    """Marque plusieurs factures comme non payées en une fois"""
    queryset.update(payee=False)

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    """Interface d'administration pour les factures avec actions en lot"""
    list_display = ('numero', 'client', 'montant', 'payee')
    list_filter = ('client', 'payee')  # Filtres latéraux
    search_fields = ('numero', 'client__nom')  # Recherche dans numéro et nom client
    actions = [marquer_comme_paye, marquer_comme_non_paye]
    readonly_fields = ['numero', 'date']  # Champs non modifiables

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    """Interface simple pour les catégories"""
    pass

@admin.register(HistoriqueFacture)
class HistoriqueFactureAdmin(admin.ModelAdmin):
    """Interface de consultation de l'historique (lecture seule)"""
    list_display = ('facture', 'action', 'date_action')
    list_filter = ('date_action',)
    readonly_fields = ('facture', 'action', 'date_action')