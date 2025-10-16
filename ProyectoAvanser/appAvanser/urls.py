from rest_framework.routers import DefaultRouter
from .views import CitaComiteViewSet, AsignacionFichaViewSet, ReporteTrimestralViewSet, ActividadViewSet,FichaBusquedaView,NotificacionViewSet
from django.urls import path, include

router = DefaultRouter()
#HU008 - Rutas para CitaComite (Administrador, Funcionario de Bienestar)
router.register(r"comites", CitaComiteViewSet, basename="comite")
#HU010 - Rutas para busqueda fichas y notificaciones (Instructor, Aprendiz)
router.register(r"asignaciones", AsignacionFichaViewSet, basename="asignacion") 
router.register(r"notificaciones", NotificacionViewSet, basename="notificacion")  

#HU012 - Rutas para Reporte Trimestral (Instructor)

router.register(r"reportes", ReporteTrimestralViewSet, basename="reporte")
router.register(r"actividades", ActividadViewSet, basename="actividad")


#router.register(r"fichas-busqueda", FichaBusquedaView, basename="ficha-busqueda")

urlpatterns = router.urls + [
    # Ruta para búsqueda de fichas (APIView)
    path("fichas/buscar/", FichaBusquedaView.as_view(), name="buscar-fichas"),
]


