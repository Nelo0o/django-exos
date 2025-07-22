from django.test import TestCase
from django.urls import reverse
from .models import Facture, Categorie
from clients.models import Client
from decimal import Decimal

class FactureModelTest(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(nom="Test Client", email="test@example.com")
        self.categorie = Categorie.objects.create(nom="Services")

    def test_creation_facture_valide(self):
        facture = Facture.objects.create(
            numero="F001",
            montant=Decimal('100.00'),
            tax=Decimal('20.00'),
            client=self.client_obj,
            categorie=self.categorie
        )
        self.assertEqual(facture.numero, "F001")
        self.assertEqual(facture.montant, Decimal('100.00'))
        self.assertEqual(facture.tax, Decimal('20.00'))
        self.assertEqual(facture.client, self.client_obj)
        self.assertEqual(facture.categorie, self.categorie)

    def test_montant_ttc_calcul_auto(self):
        facture = Facture.objects.create(
            numero="F002",
            montant=Decimal('200.00'),
            tax=Decimal('10.00'),
            client=self.client_obj,
            categorie=self.categorie
        )
        # montant_ttc = montant * (1 + tax/100)
        self.assertEqual(facture.montant_ttc, Decimal('220.00'))

    def test_str_method(self):
        facture = Facture.objects.create(
            numero="F003",
            montant=Decimal('50.00'),
            tax=Decimal('20.00'),
            client=self.client_obj,
            categorie=self.categorie
        )
        self.assertIn("Facture F003", str(facture))
        self.assertIn("€", str(facture))

    def test_categorie_automatique_autres(self):
        facture = Facture.objects.create(
            numero="F004",
            montant=Decimal('80.00'),
            tax=Decimal('20.00'),
            client=self.client_obj
            # Pas de catégorie ici
        )
        self.assertEqual(facture.categorie.nom, "Autres")

class FactureListViewTest(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(nom="Client Vue", email="vue@example.com")
        self.categorie = Categorie.objects.create(nom="Catégorie Vue")
        self.facture1 = Facture.objects.create(
            numero="L001", montant=Decimal('100.00'), tax=Decimal('20.00'), client=self.client_obj, categorie=self.categorie
        )
        self.facture2 = Facture.objects.create(
            numero="L002", montant=Decimal('200.00'), tax=Decimal('10.00'), client=self.client_obj, categorie=self.categorie
        )

    def test_list_view_status_code(self):
        url = reverse('facture-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        url = reverse('facture-list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'factures/facture_list.html')

    def test_list_view_content(self):
        url = reverse('facture-list')
        response = self.client.get(url)
        self.assertContains(response, "L001")
        self.assertContains(response, "L002")

class FactureDetailViewTest(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(nom="Client Detail", email="detail@example.com")
        self.categorie = Categorie.objects.create(nom="Catégorie Detail")
        self.facture = Facture.objects.create(
            numero="D001", montant=Decimal('150.00'), tax=Decimal('15.00'), client=self.client_obj, categorie=self.categorie
        )

    def test_detail_view_status_code(self):
        url = reverse('facture-detail', args=[self.facture.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view_template(self):
        url = reverse('facture-detail', args=[self.facture.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'factures/facture_detail.html')

    def test_detail_view_content(self):
        url = reverse('facture-detail', args=[self.facture.pk])
        response = self.client.get(url)
        self.assertContains(response, "D001")
        self.assertContains(response, "150.00")

class FactureCreateViewTest(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(nom="Client Créa", email="crea@example.com")
        self.categorie = Categorie.objects.create(nom="Catégorie Créa")

    def test_create_view_status_code(self):
        url = reverse('facture-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        url = reverse('facture-create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'factures/facture_form.html')

    def test_create_facture_post(self):
        url = reverse('facture-create')
        data = {
            'numero': 'C001',
            'montant': '300.00',
            'tax': '20.00',
            'client': self.client_obj.pk,
            'categorie': self.categorie.pk,
            'commentaires': 'Test création',
            'payee': False
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Facture.objects.filter(numero='C001').exists())
        self.assertContains(response, 'C001')
