from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.contrib.auth.models import User
from apps.projectsapp.models import Project


class ProjectsTest(APITestCase):
    def setUp(self):
        User(username='user').save()
        self.client = APIClient()
        client_token = Token.objects.get(user__username='user')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {client_token}')

        self.project_payload = {
            "name": "Superman"
        }

        self.update_own_project_payload = {
            "name": "Different name."
        }

    def test_get_projects(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        response = self.client.post(
            '/api/projects/',
            self.project_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_project(self):
        response = self.client.post(
            '/api/projects/',
            self.project_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        p = Project.objects.get(name='Superman')
        response = self.client.get(f'/api/projects/{p.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_own_project(self):
        create_response = self.client.post(
            '/api/projects/',
            self.project_payload,
            format='json'
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        p = Project.objects.get(name='Superman')
        response = self.client.put(
            f'/api/projects/{p.id}/',
            self.update_own_project_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_not_own_project(self):
        User(username='stranger').save()
        stranger_token = Token.objects.get(user__username='stranger')
        stranger = APIClient()
        stranger.credentials(HTTP_AUTHORIZATION=f'Token {stranger_token.key}')

        create_response = self.client.post(
            '/api/projects/',
            self.project_payload,
            format='json'
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        p = Project.objects.get(name='Superman')
        response = stranger.put(
            f'/api/projects/{p.id}/',
            self.update_own_project_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
