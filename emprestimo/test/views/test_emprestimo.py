from datetime import date
from decimal import Decimal
from emprestimo.models.emprestimo import Emprestimo
from emprestimo.models.pagamento import Pagamento
from emprestimo.test.base.base_api_test_case import BaseAPITestCase

class EmprestimoViewTest(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.emprestimo = Emprestimo.objects.create(
            usuario=self.user,
            valor_nominal=Decimal("1000.00"),
            taxa_juros=Decimal("0.05"),
            banco="GPA",
            cliente="Gloria Almeida",
            ip_cadastro="127.0.0.1",
            data_solicitacao=date.today()
        )

    def test_listar_emprestimos(self):
        response = self.client.get("/api/emprestimos/")
        self.assertEqual(response.status_code, 200)

    def test_saldo_devedor(self):
        url = f"/api/emprestimos/{self.emprestimo.id}/saldo_devedor/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("saldo_devedor", response.data)

    def test_adicionar_pagamento(self):
        url = f"/api/emprestimos/{self.emprestimo.id}/adicionar_pagamento/"
        data = {"valor_pagamento": 100.00, "data_pagamento": "2025-10-20"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pagamento.objects.count(), 1)

    def test_usuario_nao_pode_adicionar_pagamento_em_emprestimo_de_outro_usuario(self):
        outro_emprestimo = Emprestimo.objects.create(
            usuario=self.outro_user,
            valor_nominal=Decimal("1500.00"),
            taxa_juros=Decimal("0.04"),
            banco="REAL",
            cliente="Graciela Almeida",
            ip_cadastro="127.0.0.2",
            data_solicitacao=date.today()
        )
        url = f"/api/emprestimos/{outro_emprestimo.id}/adicionar_pagamento/"
        data = {"valor_pagamento": "100.00", "data_pagamento": "2025-09-20"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
