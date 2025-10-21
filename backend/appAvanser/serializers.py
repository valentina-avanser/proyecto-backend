from rest_framework import serializers
from .models import *


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['documento', 'username', 'first_name', 'last_name','email']
        depth = 2

class ProgramaFormacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaFormacion
        fields = '__all__'
        depth = 2

class FichaSerializer(serializers.ModelSerializer):
    programa = serializers.PrimaryKeyRelatedField(queryset=ProgramaFormacion.objects.all())
    class Meta:
        model = Ficha
        fields = ['id', 'numero_ficha','programa', 'jornada', 'fecha_inicio', 'fecha_fin','instructor_lider','instructores']

class AprendizSerializer(serializers.ModelSerializer):
    apUsuario = UsuarioSerializer()
    ficha = serializers.PrimaryKeyRelatedField(queryset=Ficha.objects.all())

    class Meta:
        model = Aprendiz
        fields = ['id', 'ficha', 'estado', 'fecha_ingreso', 'fecha_egreso', 'apUsuario']

    def create(self, validated_data):
        # Extraer los datos anidados del usuario
        usuario_data = validated_data.pop('apUsuario')
        # Crear el usuario primero
        usuario = Usuario.objects.create(**usuario_data)
        # Crear el aprendiz con el usuario asociado
        aprendiz = Aprendiz.objects.create(apUsuario=usuario, **validated_data)
        return aprendiz

class InstructorSerializer(serializers.ModelSerializer):
    instUsuario = UsuarioSerializer()
    class Meta:
        model = Instructor
        fields = ['instUsuario', 'especialidad']

    def create(self, validated_data):
        usuario_data = validated_data.pop('instUsuario')
        usuario = UsuarioSerializer().create(usuario_data)
        instructor = Instructor.objects.create(instUsuario=usuario, **validated_data)
        return instructor

class FuncionarioSerializer(serializers.ModelSerializer):
    funcUsuario = UsuarioSerializer()
    class Meta:
        model = Funcionario
        fields = ['funcUsuario', 'cargo']

class CoordinadorBienestarSerializer(serializers.ModelSerializer):
    coordBienestarUsuario = UsuarioSerializer()
    class Meta:
        model = CoordinadorBienestar
        fields = ['coordBienestarUsuario']

class CoordinadorInstructoresSerializer(serializers.ModelSerializer):
    coordInstructoresUsuario = UsuarioSerializer()
    class Meta:
        model = CoordinadorInstructores
        fields = ['coordInstructoresUsuario']   

class TipoConvocatoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoConvocatoria
        fields = '__all__'
        depth=2  # Muestra datos de relaciones ForeignKey
        
    
class ConvocatoriaSerializer(serializers.ModelSerializer):  
    con_tipo = serializers.PrimaryKeyRelatedField(queryset=TipoConvocatoria.objects.all())  
    class Meta:
        model = Convocatoria
        fields = '__all__'
        depth=2  
        
class PostulacionSerializer(serializers.ModelSerializer):
    #posAprendiz = serializers.PrimaryKeyRelatedField(queryset=Aprendiz.objects.all())  
    #posConvocatoria = serializers.PrimaryKeyRelatedField(queryset=Convocatoria.objects.all())  
    class Meta:
        model=Postulacion
        fields='__all__'
        #depth=2
        
class ResultadoPostulacionSerializer(serializers.ModelSerializer):
    class Meta:
        model=ResultadoPostulacion
        fields='__all__'


        
