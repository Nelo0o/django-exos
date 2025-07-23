"""Signaux Django pour tracer automatiquement les actions sur les factures"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Facture, HistoriqueFacture

@receiver(post_save, sender=Facture)
def creer_historique(sender, instance, created, **kwargs):
    """Crée un historique lors de la création d'une facture"""
    if created:  # Seulement à la création
        HistoriqueFacture.objects.create(
            facture=instance,
            action=f'Création de la facture {instance.numero}'
        )
    
@receiver(post_save, sender=Facture)
def modifier_historique(sender, instance, created, **kwargs):
    """Crée un historique lors de la modification d'une facture"""
    if not created:  # Seulement lors des modifications
        HistoriqueFacture.objects.create(
            facture=instance,
            action=f'Modification de la facture {instance.numero}'
        )

@receiver(pre_delete, sender=Facture)
def supprimer_historique(sender, instance, **kwargs):
    """Crée un historique avant la suppression d'une facture"""
    HistoriqueFacture.objects.create(
        facture=instance,
        action=f'Suppression de la facture {instance.numero}'
    )