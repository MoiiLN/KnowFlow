from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Library
import json

class LibraryTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser',
            password='1234'
        )

        self.library = Library.objects.create(
            user=self.user,
            name="Test Library",
            slug="test-library",
            description="Descripción test"
        )

    def test_library_list(self):
        response = self.client.get('/api/libraries/')
        self.assertEqual(response.status_code, 200)

    def test_library_detail(self):
        response = self.client.get(f'/api/libraries/{self.library.id}/')
        self.assertEqual(response.status_code, 200)

    def test_library_not_found(self):
        response = self.client.get('/api/libraries/999/')
        self.assertEqual(response.status_code, 404)

    def test_create_library(self):
        response = self.client.post('/api/libraries/create/', {
            'name': 'Nueva Library',
            'slug': 'nueva-library',
            'description': 'desc',
            'user': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Library.objects.count(), 2)

    def test_edit_library(self):
        response = self.client.put(
            f'/api/libraries/edit/{self.library.id}/',
            data=json.dumps({
                'name': 'Editada',
                'slug': 'editada',
                'description': 'desc',
                'user': self.user.id
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.library.refresh_from_db()
        self.assertEqual(self.library.name, 'Editada')

    def test_delete_library(self):
        response = self.client.delete(
            f'/api/libraries/delete/{self.library.id}/'
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Library.objects.count(), 0)