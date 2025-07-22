from django.contrib import admin
from emprestimo.models.emprestimo import Emprestimo
from emprestimo.models.pagamento import Pagamento

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'valor_nominal', 'taxa_juros', 'data_solicitacao', 'banco', 'usuario', 'ip_cadastro']
    list_filter = ['banco', 'data_solicitacao', 'usuario']
    search_fields = ['cliente', 'banco', 'id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    
@admin.register(Pagamento)
class PagamentoEmprestimoAdmin(admin.ModelAdmin):
    list_display = ['id', 'emprestimo', 'data_pagamento', 'valor_pagamento']
    list_filter = ['emprestimo', 'data_pagamento']
    search_fields = ['cliente', 'banco', 'id']
    readonly_fields = ['id', 'created_at', 'updated_at']