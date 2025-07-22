from django.test import TestCase
from django.core.exceptions import ValidationError
from emprestimo.models.emprestimo import Emprestimo
from emprestimo.models.pagamento import Pagamento
from decimal import Decimal
from django.contrib.auth.models import User
from datetime import date

class PagamentoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="123456")
        
        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=Decimal("1000.00"),
            taxa_juros=Decimal("5.0"),
            banco="Caixa",
            cliente="Fulano da Silva",
            usuario=self.user,
            ip_cadastro="127.0.0.1",
            data_solicitacao=date.today()
        )
        self.pagamento_valido = {
            "emprestimo": self.emprestimo,
            "data_pagamento": date.today(),
            "valor_pagamento": Decimal("100.00")
        }
        
    def test_criar_pagamento_valido(self):
        pagamento = Pagamento.objects.create(
            emprestimo=self.emprestimo,
            data_pagamento=date.today(),
            valor_pagamento=Decimal("200.00")
        )
        self.assertIsInstance(pagamento, Pagamento)
        self.assertEqual(pagamento.valor_pagamento, Decimal("200.00"))
        self.assertEqual(pagamento.emprestimo, self.emprestimo)
        
    def test_valor_pagamento_minimo_valido(self):

        pagamento_data = self.pagamento_valido.copy()
        pagamento_data["valor_pagamento"] = Decimal("0.01")
        
        pagamento = Pagamento.objects.create(**pagamento_data)
        self.assertEqual(pagamento.valor_pagamento, Decimal("0.01"))
    
    def test_valor_pagamento_zero_invalido(self):
        
        pagamento_data = self.pagamento_valido.copy()
        pagamento_data["valor_pagamento"] = Decimal("0.00")
        
        pagamento = Pagamento(**pagamento_data)
        
        with self.assertRaises(ValidationError):
            pagamento.full_clean()
    
    def test_valor_pagamento_negativo_invalido(self):
        
        pagamento_data = self.pagamento_valido.copy()
        pagamento_data["valor_pagamento"] = Decimal("-10.00")
        
        pagamento = Pagamento(**pagamento_data)
        
        with self.assertRaises(ValidationError):
            pagamento.full_clean()