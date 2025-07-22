from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from .views import EmprestimoViewSet, PagamantoViewSet

router = DefaultRouter()
router.register(r"emprestimos", EmprestimoViewSet, basename="emprestimos")
router.register(r"pagamentos", PagamantoViewSet, basename="pagamentos")

urlpatterns = [
    path("api/", include(router.urls))
]
