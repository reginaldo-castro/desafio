from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from .emprestimo import Emprestimo

class Pagamento(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emprestimo = models.ForeignKey(Emprestimo, on_delete=models.CASCADE, related_name='pagamentos')
    data_pagamento = models.DateField()
    valor_pagamento = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-data_pagamento']
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
    
    def __str__(self):
        return f"Pagamento {self.id} - R$ {self.valor_pagamento}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.data_pagamento and self.emprestimo:
            if self.data_pagamento < self.emprestimo.data_solicitacao:
                raise ValidationError(
                    'Data de pagamento não pode ser anterior à data de solicitação do empréstimo'
                )
