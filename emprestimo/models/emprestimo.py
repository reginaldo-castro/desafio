from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid

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
        pass
    
    def calcular_juros_periodo(self, data_inicio, data_fim):
        pass