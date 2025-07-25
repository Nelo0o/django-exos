from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Facture, Categorie
from clients.models import Client
from .forms import FactureForm

class FactureFormMixin:
    """Mixin pour partager la configuration commune des formulaires de facture"""
    model = Facture
    form_class = FactureForm
    template_name = 'factures/facture_form.html'
    success_url = reverse_lazy('facture-list')

class FactureListView(ListView):
    model = Facture
    template_name = 'factures/facture_list.html'

    def get_queryset(self):
        """Applique les filtres dynamiques selon les paramètres GET"""
        queryset = super().get_queryset()
        
        # Construction dynamique des filtres
        filters = {}
        if client_id := self.request.GET.get('client'):  # Walrus operator pour assignation + test, très pratique
            filters['client_id'] = client_id
        if categorie_id := self.request.GET.get('categorie'):
            filters['categorie_id'] = categorie_id
            
        return queryset.filter(**filters) if filters else queryset

    def get_context_data(self, **kwargs):
        """Ajoute les données nécessaires pour les filtres et statistiques"""
        context = super().get_context_data(**kwargs)
        # Données pour les filtres
        context['clients'] = Client.objects.all()
        context['categories'] = Categorie.objects.all()
        context['selected_client'] = self.request.GET.get('client', '')
        context['selected_categorie'] = self.request.GET.get('categorie', '')
        
        return context

class FactureDetailView(DetailView):
    model = Facture
    template_name = 'factures/facture_detail.html'

class FactureCreateView(FactureFormMixin, CreateView):
    pass

class FactureUpdateView(FactureFormMixin, UpdateView):
    pass

class FactureDeleteView(DeleteView):
    model = Facture
    template_name = 'factures/facture_confirm_delete.html'
    success_url = reverse_lazy('facture-list')