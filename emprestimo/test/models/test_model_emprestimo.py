from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from emprestimo.models.emprestimo import Emprestimo
from emprestimo.models.pagamento import Pagamento
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
from django.utils import timezone

class EmprestimoModelTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456')
        self.client.login(username='testuser', password='123456')

    def test_create_emprestimo(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "valor_nominal": 1000,
            "taxa_juros": 1.0,
            "banco": "Caixa",
            "cliente": "Hudson da Silva"
        }
        response = self.client.post('/api/emprestimos/', data, REMOTE_ADDR='127.0.0.1')
        self.assertEqual(response.status_code, 201)

    
    def test_calcular_saldo_devedor(self):
        """"""
        emprestimo = Emprestimo.objects.create(
            valor_nominal=1000,
            taxa_juros=2.0,
            banco="Bemol",
            cliente="Hudson da Silva",
            usuario=self.user,
            ip_cadastro="127.0.0.1"
        )
        Pagamento.objects.create(emprestimo=emprestimo, valor_pagamento=200, data_pagamento=timezone.now())
        Pagamento.objects.create(emprestimo=emprestimo, valor_pagamento=300, data_pagamento=timezone.now())  
        
        saldo_devedor = emprestimo.calcular_saldo_devedor()
        
        dias_corridos = (datetime.now().date() - emprestimo.data_solicitacao).days
        taxa_diaria = (Decimal("2.0") / Decimal("100")) / Decimal("30")
        fator_juros = (Decimal("1") + taxa_diaria) ** dias_corridos
        valor_com_juros = Decimal("1000.00") * fator_juros
        pagamentos_total = Decimal("500.00")
        saldo_esperado = valor_com_juros - pagamentos_total
        
        self.assertEqual(saldo_devedor, saldo_esperado.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        
    def test_calcular_juros_periodo(self):
        """Teste basico"""
        emprestimo = Emprestimo.objects.create(
            valor_nominal=1000,
            taxa_juros=3.0,  
            banco="Banco Teste",
            cliente="Cliente Teste",
            usuario=self.user,
            ip_cadastro="127.0.0.1"
        )
        
        data_inicio = emprestimo.data_solicitacao
        data_fim = data_inicio + timedelta(days=30)
        
        juros_calculados = emprestimo.calcular_juros_periodo(data_inicio, data_fim)
        taxa_diaria = Decimal("3.0") / Decimal("100") / Decimal("30")
        fator_juros = (Decimal("1") + taxa_diaria) ** 30
        juros_esperados = (Decimal("1000") * fator_juros - Decimal("1000")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        self.assertEqual(juros_calculados, juros_esperados)
        
    def test_calcular_juros_periodo_com_pagamentos(self):
        """Teste pagamentos feito"""
        emprestimo = Emprestimo.objects.create(
            valor_nominal=2000,
            taxa_juros=2.0,
            banco="Banco Teste",
            cliente="Cliente Teste",
            usuario=self.user,
            ip_cadastro="127.0.0.1"
        )
        
        Pagamento.objects.create(
            emprestimo=emprestimo, 
            valor_pagamento=500, 
            data_pagamento=emprestimo.data_solicitacao + timedelta(days=5)
        )
        
        data_inicio = emprestimo.data_solicitacao + timedelta(days=10)
        data_fim = data_inicio + timedelta(days=15)
        
        juros_calculados = emprestimo.calcular_juros_periodo(data_inicio, data_fim)
        
        valor_inicial = emprestimo.calcular_saldo_devedor(data_inicio)
        taxa_diaria = Decimal("2.0") / Decimal("100") / Decimal("30")
        fator_juros = (Decimal("1") + taxa_diaria) ** 15
        juros_esperados = (valor_inicial * fator_juros - valor_inicial).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
        self.assertEqual(juros_calculados, juros_esperados)
        self.assertGreater(juros_calculados, Decimal("0.00"))