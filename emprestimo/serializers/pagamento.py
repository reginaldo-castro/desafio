from rest_framework import serializers
from emprestimo.models.emprestimo import Emprestimo
from emprestimo.models.pagamento import Pagamento
from decimal import Decimal

class PagamentoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pagamento
        fields = ["id", "emprestimo", "data_pagamento", "valor_pagamento", "created_at"]
        ready_only_fields = ["id", "created_at"]
        
        