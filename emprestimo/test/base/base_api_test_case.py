from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

User = get_user_model()

class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="usuario1", password="senha1234")
        self.outro_user = User.objects.create_user(username="usuario2", password="senhau1234")
        self.client.force_authenticate(user=self.user)
