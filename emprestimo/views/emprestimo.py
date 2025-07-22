from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from emprestimo.serializers.emprestimo import EmprestimoListSerializer, EmprestimoCreateSerializer
from emprestimo.serializers.pagamento import PagamentoSerializer
from emprestimo.models.emprestimo import Emprestimo
from emprestimo.models.pagamento import Pagamento
from datetime import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status


class EmprestimoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Emprestimo.objects.filter(usuario=self.request.user).prefetch_related("pagamentos")
   
    
    def get_serializer_class(self):
        if self.action == "create":
            return EmprestimoCreateSerializer
        return EmprestimoListSerializer
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
        
    @action(detail=True, methods=["get"])
    def saldo_devedor(self, request, pk=None):
        
        emprestimo = self.get_object()
        data_calculo = request.query_params.get("data_calculo")
        
        if data_calculo:
            try:
                data_calculo = datetime.strptime(data_calculo, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"Error": "Formato de data inválido. Use DD-MM-YYYY"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        saldo = emprestimo.calcular_saldo_devedor(data_calculo)
        
        return Response({
             "emprestimo_id": emprestimo.id,
            "saldo_devedor": saldo,
            "data_calculo": data_calculo or datetime.now().date(),
            "total_pagamentos": sum(p.valor_pagamento for p in emprestimo.pagamentos.all())
        })
        
    @action(detail=True, methods=["post"])
    def adicionar_pagamento(self, request, pk=None):
        
        emprestimo = self.get_object()
        data = request.data.copy()
        data["emprestimo"] = emprestimo.id
        
        serializer = PagamentoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["get"])
    def resumo_financeiro(self, request):

        emprestimos = self.get_queryset()
        
        total_emprestimos = sum(emprestimo.valor_nominal for emprestimo in emprestimos)
        total_pagamentos = sum(
            sum(p.valor_pagamento for p in emprestimo.pagamentos.all()) 
            for emprestimo in emprestimos
        )
        saldo_devedor_total = sum(emprestimo.calcular_saldo_devedor() for emprestimo in emprestimos)
        
        return Response({
            "total_emprestimos": total_emprestimos,
            "total_pagamentos": total_pagamentos,
            "saldo_devedor_total": saldo_devedor_total,
            "quantidade_emprestimos": emprestimos.count()
        })
