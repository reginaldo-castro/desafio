from rest_framework import serializers
from emprestimo.models.emprestimo import Emprestimo
from emprestimo.models.pagamento import Pagamento
from decimal import Decimal
from emprestimo.serializers.pagamento import PagamentoListSerializer

class EmprestimoListSerializer(serializers.ModelSerializer):
    
    pagamentos = PagamentoListSerializer(many=True, read_only=True)
    cliente_nome = serializers.CharField(source="cliente.nome", read_only=True)
    banco_nome = serializers.CharField(source="banco.nome", read_only=True)
    
    class Meta:
        model = Emprestimo
        fields = [
            "id", "valor_nominal", "taxa_juros", "ip_cadastro", 
            "data_solicitacao", "banco", "cliente", "created_at",
            "pagamentos", "cliente_nome", "banco_nome"
        ]
        read_only_fields = ["id", "created_at"]

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