from django.urls import path
from .views import (
    FactureListView, FactureDetailView, FactureCreateView,
    FactureUpdateView, FactureDeleteView
)

urlpatterns = [
    path('', FactureListView.as_view(), name='facture-list'),
    path('<int:pk>/', FactureDetailView.as_view(), name='facture-detail'),
    path('ajouter/', FactureCreateView.as_view(), name='facture-create'),
    path('<int:pk>/modifier/', FactureUpdateView.as_view(), name='facture-update'),
    path('<int:pk>/supprimer/', FactureDeleteView.as_view(), name='facture-delete'),
]