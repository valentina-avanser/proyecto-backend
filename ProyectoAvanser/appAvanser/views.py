from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, permissions, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CitaComite, Ficha, AprendizFicha, Notificacion, Instructor, AsignacionFicha, ReporteTrimestral, Actividad
from .serializers import CitaComiteSerializer, FichaSerializer, NotificacionSerializer,AsignacionFichaSerializer, ReporteTrimestralSerializer, ActividadSerializer



#HU008 - ViewSet para CitaComite (Administrador, Funcionario de Bienestar)
class CitaComiteViewSet(viewsets.ModelViewSet):
    queryset = CitaComite.objects.all().order_by("-fecha_creacion")
    serializer_class = CitaComiteSerializer

    def perform_create(self, serializer):
        serializer.save(creada_por=self.request.user)

    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        cita = self.get_object()
        cita.estado = "cancelada"
        cita.save()
        return Response({"status": "Cita cancelada"}, status=status.HTTP_200_OK)


#HU010 - ViewSet para busqueda fichas y notificaciones (Instructor, Aprendiz)

class AsignacionFichaViewSet(viewsets.ModelViewSet):
    queryset = AsignacionFicha.objects.all().select_related("instructor", "ficha", "ficha__programa")
    serializer_class = AsignacionFichaSerializer

    # Solo mostrar fichas del instructor autenticado
    def get_queryset(self):
        user = self.request.user
        if user.rol.nombre_rol.lower() == "instructor":
            return AsignacionFicha.objects.filter(instructor=user)
        return AsignacionFicha.objects.none()

    @action(detail=False, methods=["get"])
    def tablero(self, request):
        """
        Retorna las fichas asignadas al instructor autenticado,
        separadas por estado.
        """
        user = request.user
        if user.rol.nombre_rol.lower() != "instructor":
            return Response({"detail": "No autorizado"}, status=403)

        activas = AsignacionFicha.objects.filter(instructor=user, estado="activa")
        deshabilitadas = AsignacionFicha.objects.filter(instructor=user, estado="deshabilitada")

        data = {
            "fichas_activas": AsignacionFichaSerializer(activas, many=True).data,
            "fichas_deshabilitadas": AsignacionFichaSerializer(deshabilitadas, many=True).data
        }
        return Response(data)


#HU010 - ViewSet para busqueda fichas y notificaciones (Instructor, Aprendiz)
class FichaBusquedaView(generics.ListAPIView):
    """
    Permite a instructores o administradores buscar fichas por número, programa o jornada.
    """
    queryset = Ficha.objects.all().select_related("programa")
    serializer_class = FichaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["numero_ficha", "programa__nombre", "jornada"]

    def get_queryset(self):
        user = self.request.user
        if user.rol.nombre_rol.lower() == "instructor":
            # Mostrar solo las fichas asignadas al instructor
            return Ficha.objects.filter(asignaciones__instructor=user)
        return super().get_queryset()
    
    
#HU010 - ViewSet para busqueda fichas y notificaciones (Instructor, Aprendiz)
class NotificacionViewSet(viewsets.ModelViewSet):
    """
    Permite listar, crear y marcar como leídas las notificaciones del usuario.
    """
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

    def get_queryset(self):
        # Solo muestra las notificaciones del usuario autenticado
        user = self.request.user
        return Notificacion.objects.filter(usuario=user).order_by("-fecha_creacion")

    @action(detail=True, methods=["post"])
    def marcar_leida(self, request, pk=None):
        notificacion = self.get_object()
        notificacion.leida = True
        notificacion.save()
        return Response({"status": "Notificación marcada como leída"})

#HU012 Reporte Trimestral

class ReporteTrimestralViewSet(viewsets.ModelViewSet):
    queryset = ReporteTrimestral.objects.all().order_by("-fecha_cargue")
    serializer_class = ReporteTrimestralSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all().order_by("-fecha_creacion")
    serializer_class = ActividadSerializer

    def get_queryset(self):
        user = self.request.user
        if user.rol.nombre_rol.lower() == "instructor":
            return Actividad.objects.filter(instructor=user)
        elif user.rol.nombre_rol.lower() == "aprendiz":
            return Actividad.objects.filter(aprendiz=user)
        return Actividad.objects.none()
