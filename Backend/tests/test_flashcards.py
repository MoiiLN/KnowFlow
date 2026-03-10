import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from flowcards.models import FlowCard

from library.models import Library, LibraryContent

User = get_user_model()


class FlowCardAPITest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpass123')

        self.client.login(username='testuser', password='testpass123')

        self.library = Library.objects.create(
            user=self.user, name='Test Library', slug='test-library'
        )

        self.library_content = LibraryContent.objects.create(
            user=self.user,
            library=self.library,
            title='Flowcard content',
            slug='flowcard-content',
            content_type='flowcard',
        )

        self.flowcard = FlowCard.objects.create(
            user=self.user,
            library=self.library_content,
            name='Card 1',
            slug='card-1',
            term='CPU',
            definition='Central Processing Unit',
        )

    def test_flowcard_list(self):
        """GET /flowcards/ devuelve las flashcards del usuario"""

        response = self.client.get('/api/flowcards/')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Card 1')

    def test_flowcard_detail(self):
        """GET detalle de una flashcard"""

        response = self.client.get('/api/flowcards/card-1/')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['term'], 'CPU')
        self.assertEqual(data['definition'], 'Central Processing Unit')

    def test_add_flowcard(self):
        """POST crear flashcard"""

        payload = {
            'library_content_id': self.library_content.id,
            'name': 'Card 2',
            'slug': 'card-2',
            'term': 'RAM',
            'definition': 'Random Access Memory',
        }

        response = self.client.post(
            '/api/flowcards/add/', data=json.dumps(payload), content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(FlowCard.objects.filter(slug='card-2').exists(), True)

    def test_edit_flowcard(self):
        """PUT editar flashcard"""

        payload = {'term': 'CPU UPDATED'}

        response = self.client.put(
            '/api/flowcards/card-1/edit/', data=json.dumps(payload), content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.flowcard.refresh_from_db()
        self.assertEqual(self.flowcard.term, 'CPU UPDATED')

    def test_play_flowcard(self):
        """GET play flowcard"""

        response = self.client.get('/api/flowcards/card-1/play/')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEqual(data['term'], 'CPU')
        self.assertEqual(data['definition'], 'Central Processing Unit')
