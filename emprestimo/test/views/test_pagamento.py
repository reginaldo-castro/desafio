from django.urls import reverse
from rest_framework import status
from emprestimo.models.emprestimo import Emprestimo
from emprestimo.models.pagamento import Pagamento
from datetime import date
from decimal import Decimal
from emprestimo.test.base.base_api_test_case import BaseAPITestCase

class PagamentoViewTest(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=Decimal("1000"),
            taxa_juros=Decimal("2.0"),
            banco="Caixa",
            cliente="Raimundo dos Santos",
            usuario=self.user,
            ip_cadastro="127.0.0.1",
            data_solicitacao=date(2025, 1, 1)
        )
        self.pagamento_url = reverse('pagamentos-list')

    def test_criar_pagamento(self):
        data = {
            "valor_pagamento": 200.00,
            "data_pagamento": "2025-09-22",
            "emprestimo": str(self.emprestimo.id)
        }
        response = self.client.post(self.pagamento_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listar_pagamentos(self):
        Pagamento.objects.create(
            valor_pagamento=150,
            data_pagamento="2025-09-22",
            emprestimo=self.emprestimo
        )
        response = self.client.get(self.pagamento_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_pagamento_de_outro_usuario(self):
        outro_emprestimo = Emprestimo.objects.create(
            valor_nominal=500,
            taxa_juros=1.5,
            banco="Caixa",
            cliente="Selina",
            usuario=self.outro_user,
            ip_cadastro="127.0.0.1",
            data_solicitacao=date(2025, 1, 1)
        )
        data = {
            "valor_pagamento": 100.00,
            "data_pagamento": "2025-08-22",
            "emprestimo": str(outro_emprestimo.id)
        }
        response = self.client.post(self.pagamento_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Empréstimo não encontrado", str(response.data))

    def test_campo_emprestimo_obrigatorio(self):
        data = {
            "valor_pagamento": 100.00,
            "data_pagamento": "2025-09-22"
        }
        response = self.client.post(self.pagamento_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("emprestimo", response.data)
