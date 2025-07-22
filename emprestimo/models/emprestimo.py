from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal, ROUND_HALF_UP
import uuid
from datetime import datetime, timedelta

class Emprestimo(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emprestimos')
    valor_nominal = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    taxa_juros = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('99.99'))],
        help_text="Taxa de juros mensal em percentual"
    )
    ip_cadastro = models.GenericIPAddressField()
    data_solicitacao = models.DateField(auto_now_add=True)
    banco = models.CharField(max_length=200)
    cliente = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Empréstimo'
        verbose_name_plural = 'Empréstimos'
    
    def __str__(self):
        return f"Empréstimo {self.id} - {self.cliente} - R$ {self.valor_nominal}"
    
    def calcular_saldo_devedor(self, data_calculo=None):
        
        
        if data_calculo is None:
         data_calculo = datetime.now().date()
        
        if data_calculo < self.data_solicitacao:
            return Decimal("0.00")
        
        dias_corridos = (data_calculo - self.data_solicitacao).days
        taxa_diaria = (Decimal(str(self.taxa_juros)) / Decimal("100")) / Decimal("30")

        fator_juros = (Decimal("1") + taxa_diaria) ** dias_corridos
        valor_com_juros = self.valor_nominal * fator_juros
        
        pagamentos_realizados = self.pagamentos.aggregate(
            total=models.Sum("valor_pagamento")
        )["total"] or Decimal("0.00")
        
        saldo_devedor = valor_com_juros - pagamentos_realizados
        
        return max(saldo_devedor, Decimal("0.00")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        
    def calcular_juros_periodo(self, data_inicio, data_fim):
        if data_fim <= data_inicio:
            return Decimal("0.00")
        
        dias_periodo = (data_fim - data_inicio).days
        taxa_diaria = (Decimal(str(self.taxa_juros)) / Decimal("100")) / Decimal("30")
        
        valor_inicial = self.calcular_saldo_devedor(data_inicio)
        fator_juros = (Decimal("1") + taxa_diaria) ** dias_periodo
        valor_final = valor_inicial * fator_juros
        
        return (valor_final - valor_inicial).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        