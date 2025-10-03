from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from .models import Administrador, Instructor, Aprendiz, Ficha, ReporteAcademico, Usuario
from .serializers import AdministradorSerializer, InstructorSerializer, AprendizSerializer, FichaSerializer, ReporteAcademicoSerializer, PerfilInstructorSerializer, EditarUsuarioSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsApplicationAdmin, IsInstructor

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    
class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    
class AprendizViewSet(viewsets.ModelViewSet):
    queryset = Aprendiz.objects.all()
    serializer_class = AprendizSerializer
    
class FichaViewSet(viewsets.ModelViewSet):
    queryset = Ficha.objects.all()
    serializer_class = FichaSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return Ficha
        return FichaSerializer
    
class ReporteAcademicoViewSet(viewsets.ReadOnlyModelViewSet):
 queryset = ReporteAcademico.objects.all() 
serializer_class = ReporteAcademicoSerializer
permission_classes = [IsApplicationAdmin] 

class EditarUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
       
        fields = ('email', 'nombre', 'apellido') 


class PerfilInstructorSerializer(serializers.ModelSerializer):
   
    usuario = EditarUsuarioSerializer()

    class Meta:
        model = Instructor
 
        fields = ('id', 'usuario', 'especialidad') 
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        usuario_data = validated_data.pop('usuario', {})
        usuario_instance = instance.usuario

 
        if usuario_data:
            usuario_instance.email = usuario_data.get('email', usuario_instance.email)
            usuario_instance.first_name = usuario_data.get('nombre', usuario_instance.first_name) 
            usuario_instance.last_name = usuario_data.get('apellido', usuario_instance.last_name) 
            usuario_instance.save()
        
        instance.especialidad = validated_data.get('especialidad', instance.especialidad)
        instance.save()

        return instance
    
class PerfilInstructorViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated] 

    @action(detail=False, methods=['get', 'put'], url_path='perfil')
    def gestionar_perfil(self, request):
        try:
            instructor = Instructor.objects.get(usuario=request.user)
        except Instructor.DoesNotExist:
            return Response({"detail": "No se encontró el perfil de instructor."}, 
                            status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = PerfilInstructorSerializer(instructor)
            return Response(serializer.data)
        elif request.method == 'PUT':
            if not request.data.get('confirmar_cambio', False):
                 return Response({"error": "Se requiere el campo 'confirmar_cambio': true para guardar los datos."}, 
                                 status=status.HTTP_400_BAD_REQUEST)

            serializer = PerfilInstructorSerializer(instructor, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    "mensaje": "Perfil actualizado exitosamente. ✅",
                    "datos": serializer.data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
