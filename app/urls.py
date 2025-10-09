from rest_framework.routers import DefaultRouter
from .views import AdministradorViewSet, InstructorViewSet, AprendizViewSet, FichaViewSet, PerfilInstructorViewSet
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register(r'administradores', AdministradorViewSet) 
router.register(r'instructores', InstructorViewSet)
router.register(r'aprendices', AprendizViewSet)
router.register(r'fichas', FichaViewSet)
router.register(r'instructor-perfil', PerfilInstructorViewSet, basename='instructor-perfil')
urlpatterns = router.urls

urlpatterns = [
     path('', include(router.urls)),
]