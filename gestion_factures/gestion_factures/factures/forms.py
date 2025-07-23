from django import forms
from .models import Facture

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['numero', 'montant', 'tax', 'client', 'categorie', 'commentaires', 'payee']
        # Configuration des widgets pour une meilleure UX
        widgets = {
            'numero': forms.TextInput(attrs={'readonly': True}),  # Non modifiable
            'tax': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),  # TVA avec contraintes
            'montant': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),  # Montant avec décimales
            'commentaires': forms.Textarea(attrs={'rows': 3}),  # Zone de texte compacte
        }
        labels = {
            'numero': 'Numéro (auto)',
            'tax': 'Taux de TVA (%)',
            'montant': 'Montant HT (€)',
            'payee': 'Facture payée',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configuration différente selon création ou modification
        if self.instance.pk:  # Modification d'une facture existante
            self.fields['numero'].help_text = "Numéro généré automatiquement (non modifiable)"
        else:  # Création d'une nouvelle facture
            from datetime import datetime
            from .models import Facture
            year = datetime.now().year
            count = Facture.objects.filter(numero__startswith=f"FAC-{year}").count() + 1
            futur_numero = f"FAC-{year}-{count:03d}"
            # Pré-remplissage du numéro pour aperçu
            self.fields['numero'].widget.attrs['value'] = futur_numero
            self.fields['numero'].help_text = "Généré automatiquement"