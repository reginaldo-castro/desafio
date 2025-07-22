from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from .views import EmprestimoViewSet

router = DefaultRouter()
router.register(r"emprestimos", EmprestimoViewSet, basename="emprestimos")

urlpatterns = [
    path("api/", include(router.urls))
]
