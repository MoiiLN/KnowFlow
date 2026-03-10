import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from library.models import Library, LibraryContent
from notes.models import Note

User = get_user_model()


class NoteAPITest(TestCase):
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
            title='Note Content',
            slug='note-content',
            content_type='note',
        )

        self.note = Note.objects.create(
            user=self.user,
            library=self.library_content,
            title='First Note',
            slug='first-note',
            content='This is a test note',
        )

    def test_note_list(self):
        """GET lista de notas"""

        response = self.client.get('/api/notes/')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'First Note')

    def test_note_detail(self):
        """GET detalle de nota"""

        response = self.client.get('/api/notes/first-note/')

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEqual(data['title'], 'First Note')
        self.assertEqual(data['content'], 'This is a test note')

    def test_add_note(self):
        """POST crear nota"""

        payload = {
            'library_content_id': self.library_content.id,
            'title': 'Second Note',
            'slug': 'second-note',
            'content': 'Another note',
        }

        response = self.client.post(
            '/api/notes/add/', data=json.dumps(payload), content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

        self.assertTrue(Note.objects.filter(slug='second-note').exists())

    def test_edit_note(self):
        """PUT editar nota"""

        payload = {'content': 'Updated content'}

        response = self.client.put(
            '/api/notes/first-note/edit/', data=json.dumps(payload), content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.note.refresh_from_db()

        self.assertEqual(self.note.content, 'Updated content')
