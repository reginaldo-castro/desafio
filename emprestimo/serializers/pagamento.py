from rest_framework import serializers
from emprestimo.models.emprestimo import Emprestimo
from emprestimo.models.pagamento import Pagamento
from decimal import Decimal

class PagamentoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pagamento
        fields = ["id", "emprestimo", "data_pagamento", "valor_pagamento", "created_at"]
        ready_only_fields = ["id", "created_at"]
        
    def validate_valor_pagamento(self, value):
        
        if value <= 0:
            raise serializers.ValidationError("Valor do pagamento deve ser positivo")
        return value
    
    def validate(self, data):
        
        emprestimo = data.get("emprestimo")
        data_pagamento = data.get("data_pagamento")
        
        if emprestimo and data_pagamento:
            if data_pagamento < emprestimo.data_solicitacao:
                raise serializers.ValidateError(
                    "Data de pagamento não pode ser anterior à data de solicitação"
                )
                
        return data