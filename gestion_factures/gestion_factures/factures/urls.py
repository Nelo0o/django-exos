from django.urls import path
from .views import (
    FactureListView, FactureDetailView, FactureCreateView,
    FactureUpdateView, FactureDeleteView
)

# URLs pour la gestion des factures - CRUD complet
urlpatterns = [
    path('', FactureListView.as_view(), name='facture-list'),  # Liste avec filtres
    path('<int:pk>/', FactureDetailView.as_view(), name='facture-detail'),  # Détail facture
    path('ajouter/', FactureCreateView.as_view(), name='facture-create'),  # Nouvelle facture
    path('<int:pk>/modifier/', FactureUpdateView.as_view(), name='facture-update'),  # Modification
    path('<int:pk>/supprimer/', FactureDeleteView.as_view(), name='facture-delete'),  # Suppression
]