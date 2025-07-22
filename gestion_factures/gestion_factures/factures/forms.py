from django import forms
from .models import Facture

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['numero', 'montant', 'tax', 'client', 'categorie', 'commentaires', 'payee']
        widgets = {
            'tax': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),
            'montant': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'commentaires': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'tax': 'Taux de TVA (%)',
            'montant': 'Montant HT (€)',
        }