from django.contrib import admin
from .models import Facture, Categorie

@admin.action(description="Marquer comme payé")
def marquer_comme_paye(modeladmin, request, queryset):
    queryset.update(payee=True)

def marquer_comme_non_paye(modeladmin, request, queryset):
    queryset.update(payee=False)

class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero', 'client', 'montant', 'payee')
    list_filter = ('client', 'payee')
    search_fields = ('numero', 'client__nom')
    actions = [marquer_comme_paye, marquer_comme_non_paye]

admin.site.register(Facture, FactureAdmin)
admin.site.register(Categorie)