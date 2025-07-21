from rest_framework import serializers
from emprestimo.models.emprestimo import Emprestimo
from emprestimo.models.pagamento import Pagamento
from decimal import Decimal

class EmprestimoCreateSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Emprestimo
        fields = [
            'valor_nominal', 'taxa_juros', 'data_solicitacao', 
            'banco', 'cliente'
        ]
        read_only_fields = ["id", "created_at"]
    
    def create(self, validated_data):
        
        request = self.context.get('request')
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