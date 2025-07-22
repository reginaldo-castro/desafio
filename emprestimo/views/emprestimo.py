from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from emprestimo.serializers.emprestimo import EmprestimoListSerializer, EmprestimoCreateSerializer
from emprestimo.models.emprestimo import Emprestimo
from datetime import datetime
from rest_framework import viewsets

class EmprestimoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Emprestimo.objects.filter(usuario=self.request.user).prefetch_related('pagamentos')
   
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EmprestimoCreateSerializer
        return EmprestimoListSerializer
    
    
