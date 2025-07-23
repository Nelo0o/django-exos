from django.db import models
from clients.models import Client

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class HistoriqueFacture(models.Model):
    """Trace les actions effectuées sur les factures"""
    facture = models.ForeignKey('Facture', on_delete=models.SET_NULL, null=True)
    date_action = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50, default='Création')
    
    def __str__(self):
        facture_info = self.facture.numero if self.facture else "Facture supprimée"
        return f"{self.action} - {facture_info} - {self.date_action}"

class FactureManager(models.Manager):
    """Manager personnalisé pour les opérations courantes sur les factures"""
    
    def payees(self):
        """Retourne les factures payées"""
        return self.filter(payee=True)
    
    def non_payees(self):
        """Retourne les factures non payées"""
        return self.filter(payee=False)
    
    def total_montant(self):
        """Calcule le montant total de toutes les factures"""
        from django.db.models import Sum
        result = self.aggregate(total=Sum('montant_ttc'))
        return result['total'] or 0

class Facture(models.Model):
    numero = models.CharField(max_length=30, unique=True, help_text="Numéro généré automatiquement")
    date = models.DateField(auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, help_text="Montant HT en euros")
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=20.00, help_text="Taux de TVA en %")
    montant_ttc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Montant TTC calculé automatiquement")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, related_name="factures")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True, related_name="factures")
    commentaires = models.TextField(blank=True, null=True)
    payee = models.BooleanField(default=False, verbose_name="Payée")
    
    class Meta:
        ordering = ['-date', '-id']
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
    
    objects = FactureManager()
    
    def save(self, *args, **kwargs):
        # Génération automatique du numéro de facture
        if not self.numero:
            from datetime import datetime
            year = datetime.now().year
            count = Facture.objects.filter(numero__startswith=f"FAC-{year}").count() + 1
            self.numero = f"FAC-{year}-{count:03d}"
        
        # Calcul automatique du montant TTC
        if self.montant and self.tax:
            self.montant_ttc = round(float(self.montant) * (1 + float(self.tax) / 100), 2)
        
        # Attribution dans la catégorie "Autres" qunad la catégorie n'est pas renseignée
        if not self.categorie:
            self.categorie, _ = Categorie.objects.get_or_create(nom="Autres")
        
        super().save(*args, **kwargs)
    


    def __str__(self):
        return f"Facture {self.numero} - {self.montant_ttc or self.montant} €"
