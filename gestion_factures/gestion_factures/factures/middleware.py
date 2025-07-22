from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Facture, HistoriqueFacture

@receiver(post_save, sender=Facture)
def creer_historique(sender, instance, created, **kwargs):
    if created:
        HistoriqueFacture.objects.create(
            facture=instance,
            action=f'Création de la facture {instance.numero}'
        )
    
@receiver(post_save, sender=Facture)
def modifier_historique(sender, instance, created, **kwargs):
    if not created:
        HistoriqueFacture.objects.create(
            facture=instance,
            action=f'Modification de la facture {instance.numero}'
        )

@receiver(pre_delete, sender=Facture)
def supprimer_historique(sender, instance, **kwargs):
    HistoriqueFacture.objects.create(
        facture=instance,
        action=f'Suppression de la facture {instance.numero}'
    )