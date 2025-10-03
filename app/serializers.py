from rest_framework import serializers
from .models import Administrador, Instructor, Aprendiz , Ficha, ReporteAcademico, AprendizFicha, Competencia, Horario, FichaHorario, FichaCompetencia, Usuario


class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__' 
        
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'
        
class AprendizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aprendiz
        fields = '__all__'
        
class FichaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ficha
        fields = '__all__' 
        
class ReporteAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteAcademico
        fields = '__all__'  
        
from rest_framework import serializers
from .models import Ficha, Instructor, Aprendiz, AprendizFicha 

class FichaCreacionSerializer (serializers.ModelSerializer):
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.all(), source='instructor', write_only=True
    )
    aprendices_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    competencias_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    horarios_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    
    class Meta:
        model = Ficha
        fields = ('numero_ficha', 'programa', 'jornada', 'fecha_inicio', 'fecha_fin', 
                  'instructor_id', 'aprendices_ids', 'competencias_ids', 'horarios_ids')

    def crear(self, validated_data):
        aprendices_ids = validated_data.pop('aprendices_ids')
        instructor = validated_data.pop('instructor')
        competencias_ids = validated_data.pop('competencias_ids') 
        horarios_ids = validated_data.pop('horarios_ids')
        
      
        ficha = Ficha.objects.create(instructor=instructor, **validated_data)
        
        
        aprendices_encontrados = Aprendiz.objects.filter(id__in=aprendices_ids)
        
       
        objetos_aprendiz_ficha = [
            AprendizFicha(
                aprendiz=a, 
                ficha=ficha,                                      
                fecha_ingreso=ficha.fecha_inicio                  
            )
            for a in aprendices_encontrados                         
        ]
        
        AprendizFicha.objects.bulk_create(objetos_aprendiz_ficha)
        
        competencias_encontradas = Competencia.objects.filter(id__in=competencias_ids)
        objetos_ficha_competencia = [
            FichaCompetencia(ficha=ficha, competencia=c)
            for c in competencias_encontradas
        ]
        FichaCompetencia.objects.bulk_create(objetos_ficha_competencia)
        
        horarios_encontrados = Horario.objects.filter(id__in=horarios_ids)
        objetos_ficha_horario = [
            FichaHorario(ficha=ficha, horario=h)
            for h in horarios_encontrados
        ]
        FichaHorario.objects.bulk_create(objetos_ficha_horario)
        
        
        return ficha 
    
class EditarUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('email','nombre', 'apellido')
        
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
            usuario_instance.first_name = usuario_data.get('first_name', usuario_instance.first_name)
            usuario_instance.last_name = usuario_data.get('last_name', usuario_instance.last_name)
            usuario_instance.save()
        
        instance.especialidad = validated_data.get('especialidad', instance.especialidad)
        instance.save()

        return instance