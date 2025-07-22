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
    # Créer l'historique de suppression avant que la facture soit supprimée
    # On ne peut pas référencer la facture car elle va être supprimée
    HistoriqueFacture.objects.create(
        facture=None,  # La facture sera supprimée, on ne peut pas la référencer
        action=f'Suppression de la facture {instance.numero}'
    )