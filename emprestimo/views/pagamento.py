from emprestimo.serializers.pagamento import PagamentoListSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from emprestimo.models.pagamento import Pagamento

class PagamantoViewSet(viewsets.ModelViewSet):
    
    permission_classes = [ IsAuthenticated]
    serializer_class = PagamentoListSerializer
    
    def get_queryset(self):
        return Pagamento.objects.filter(emprestimo__usuario=self.request.user)
    