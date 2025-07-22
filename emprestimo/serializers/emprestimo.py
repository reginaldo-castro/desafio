from rest_framework import serializers
from emprestimo.models.emprestimo import Emprestimo
from emprestimo.models.pagamento import Pagamento
from decimal import Decimal
from emprestimo.serializers.pagamento import PagamentoSerializer
from rest_framework.exceptions import ValidationError

class EmprestimoListSerializer(serializers.ModelSerializer):
    
    pagamentos = PagamentoSerializer(many=True, read_only=True)
    cliente_nome = serializers.CharField(source="cliente.nome", read_only=True)
    banco_nome = serializers.CharField(source="banco.nome", read_only=True)
    saldo_devedor = serializers.SerializerMethodField()
    
    class Meta:
        model = Emprestimo
        fields = [
            "id", "valor_nominal", "taxa_juros", "ip_cadastro", 
            "data_solicitacao", "banco", "cliente", "created_at",
            "pagamentos", "cliente_nome", "banco_nome", "saldo_devedor"
        ]
        read_only_fields = ["id", "created_at"]
    
    def get_saldo_devedor(self, obj):
        
        return obj.calcular_saldo_devedor()
    
    def get_total_pagamentos(self, obj):
        
        return sum(p.valor_pagamento for p in obj.pagamentos.all())

    def validate_valor_nominal(self, value):
        
        if value <= 0:
            raise ValidationError("Valor nominal deve ser positivo")
        return value
    
    def validate_taxa_juros(self, value):
        
        if value <= 0 or value > 99.99:
            raise ValidationError("Taxa de juros deve estar entre 0.01% e 99.99%")
        return value
     
class EmprestimoCreateSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Emprestimo
        fields = [
            "valor_nominal", "taxa_juros", "data_solicitacao", 
            "banco", "cliente"
        ]
        read_only_fields = ["id", "created_at"]
    
    def create(self, validated_data):
        
        request = self.context.get("request")
        validated_data["usuario"] = request.user
        validated_data["ip_cadastro"] = self.get_cliente_ip(request)
        return super().create(validated_data)
    
    def get_cliente_ip(self, request):
        
        ip_cliente = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip_cliente:
            ip = ip_cliente.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
            
        return ip