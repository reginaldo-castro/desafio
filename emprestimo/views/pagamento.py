from emprestimo.serializers.pagamento import PagamentoSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from emprestimo.models.pagamento import Pagamento
from rest_framework.exceptions import ValidationError

class PagamantoViewSet(viewsets.ModelViewSet):
    
    permission_classes = [ IsAuthenticated]
    serializer_class = PagamentoSerializer
    
    def get_queryset(self):
        return Pagamento.objects.filter(emprestimo__usuario=self.request.user)
    
    def perform_create(self, serializer):
        
        emprestimo = serializer.validated_data["emprestimo"]
        
        if emprestimo is None:
            raise ValidationError("O campo 'emprestimo' é obrigatório.")
        
        if emprestimo.usuario != self.request.user:
            raise ValidationError("Empréstimo não encontrado")
        serializer.save()