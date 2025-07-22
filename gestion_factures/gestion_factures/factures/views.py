from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Facture
from clients.models import Client
from .forms import FactureForm
from .models import Categorie

class FactureListView(ListView):
    model = Facture
    template_name = 'factures/facture_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.GET.get('client')
        categorie_id = self.request.GET.get('categorie')

        if client_id:
            queryset = queryset.filter(client_id=client_id)
        if categorie_id:
            queryset = queryset.filter(categorie_id=categorie_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.all()
        context['categories'] = Categorie.objects.all()
        context['selected_client'] = self.request.GET.get('client', '')
        context['selected_categorie'] = self.request.GET.get('categorie', '')
        return context

class FactureDetailView(DetailView):
    model = Facture
    template_name = 'factures/facture_detail.html'

class FactureCreateView(CreateView):
    model = Facture
    form_class = FactureForm
    template_name = 'factures/facture_form.html'
    success_url = reverse_lazy('facture-list')

class FactureUpdateView(UpdateView):
    model = Facture
    form_class = FactureForm
    template_name = 'factures/facture_form.html'
    success_url = reverse_lazy('facture-list')

class FactureDeleteView(DeleteView):
    model = Facture
    template_name = 'factures/facture_confirm_delete.html'
    success_url = reverse_lazy('facture-list')