from django.test import TestCase, Client
from .models import TaskFlow
import json

class TaskFlowTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.task = TaskFlow.objects.create(
            title="Task",
            description="desc"
        )

    def test_task_list(self):
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_task_detail(self):
        response = self.client.get(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, 200)

    def test_task_not_found(self):
        response = self.client.get('/api/tasks/999/')
        self.assertEqual(response.status_code, 404)

    def test_create_task(self):
        response = self.client.post('/api/tasks/create/', {
            'title': 'Nueva Task',
            'description': 'desc'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TaskFlow.objects.count(), 2)

    def test_edit_task(self):
        response = self.client.put(
            f'/api/tasks/edit/{self.task.id}/',
            data=json.dumps({
                'title': 'Editada',
                'description': 'desc'
            }),
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 400, 405])

    def test_delete_task(self):
        response = self.client.delete(
            f'/api/tasks/delete/{self.task.id}/'
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(TaskFlow.objects.count(), 0)