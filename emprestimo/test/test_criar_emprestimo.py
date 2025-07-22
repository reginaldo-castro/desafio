from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from emprestimo.models.emprestimo import Emprestimo

class EmprestimoTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456')
        self.client.login(username='testuser', password='123456')

    def test_create_emprestimo(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "valor_nominal": 1000,
            "taxa_juros": 1.0,
            "banco": "Caixa",
            "cliente": "Fulano da Silva"
        }
        response = self.client.post('/api/emprestimos/', data, REMOTE_ADDR='127.0.0.1')
        self.assertEqual(response.status_code, 201)
