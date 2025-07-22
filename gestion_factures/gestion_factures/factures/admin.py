from django.contrib import admin
from .models import Facture, Categorie, HistoriqueFacture

@admin.action(description="Marquer comme payé")
def marquer_comme_paye(modeladmin, request, queryset):
    queryset.update(payee=True)

@admin.action(description="Marquer comme non payé")
def marquer_comme_non_paye(modeladmin, request, queryset):
    queryset.update(payee=False)

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero', 'client', 'montant', 'payee')
    list_filter = ('client', 'payee')
    search_fields = ('numero', 'client__nom')
    actions = [marquer_comme_paye, marquer_comme_non_paye]
    readonly_fields = ['numero', 'date']

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    pass

@admin.register(HistoriqueFacture)
class HistoriqueFactureAdmin(admin.ModelAdmin):
    list_display = ('facture', 'action', 'date_action')
    list_filter = ('date_action',)
    readonly_fields = ('facture', 'action', 'date_action')