from django.db import models
from clients.models import Client

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Facture(models.Model):
    numero = models.CharField(max_length=30)
    date = models.DateField(auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=20.00, help_text="Taux de TVA en %")
    montant_ttc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Montant TTC calculé automatiquement")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, related_name="factures")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True, blank=True, related_name="factures")
    commentaires = models.TextField(blank=True, null=True)
    payee = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.montant and self.tax:
            self.montant_ttc = self.montant * (1 + self.tax / 100)
        
        if not self.categorie:
            autres_categorie, _ = Categorie.objects.get_or_create(
                nom="Autres"
            )
            self.categorie = autres_categorie
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Facture {self.numero} - {self.montant_ttc or self.montant} €"
