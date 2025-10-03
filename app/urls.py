from rest_framework.routers import DefaultRouter
from .views import AdministradorViewSet, InstructorViewSet, AprendizViewSet, FichaViewSet, PerfilInstructorViewSet

router = DefaultRouter()

router.register(r'administradores', AdministradorViewSet) 
router.register(r'instructores', InstructorViewSet)
router.register(r'aprendices', AprendizViewSet)
router.register(r'fichas', FichaViewSet)
router.register(r'instructor-perfil', PerfilInstructorViewSet, basename='instructor-perfil')
urlpatterns = router.urls

urlpatterns = router.urls