from django.test import TestCase, Client
from django.urls import reverse
from .models import Knowtionary

class KnowtionaryTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.knowtionary = Knowtionary.objects.create(
            name="Test Know",
            slug="test-know",
            description="Descripción de prueba"
        )

    # 🔹 TEST LISTADO
    def test_knowtionary_list(self):
        response = self.client.get('/api/knowtionaries/')

        self.assertEqual(response.status_code, 200)

    # 🔹 TEST DETALLE
    def test_knowtionary_detail(self):
        response = self.client.get(f'/api/knowtionaries/{self.knowtionary.id}/')

        self.assertEqual(response.status_code, 200)

    # 🔹 TEST DETALLE NO EXISTE
    def test_knowtionary_not_found(self):
        response = self.client.get('/api/knowtionaries/999/')

        self.assertEqual(response.status_code, 404)

    # 🔹 TEST CREAR
    def test_create_knowtionary(self):
        response = self.client.post('/api/knowtionaries/add/', {
            'name': 'Nuevo',
            'slug': 'nuevo',
            'description': 'desc'
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Knowtionary.objects.count(), 2)

    # 🔹 TEST EDITAR
    def test_edit_knowtionary(self):
        import json

        response = self.client.put(
            '/api/knowtionaries/edit/',
            data=json.dumps({
                'id': self.knowtionary.id,
                'name': 'Editado'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.knowtionary.refresh_from_db()
        self.assertEqual(self.knowtionary.name, 'Editado')