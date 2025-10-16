from rest_framework import serializers
from .models import CitaComite, Usuario,Ficha, AprendizFicha, Notificacion, AsignacionFicha, Ficha,ReporteTrimestral, Actividad

#HU008 - Serializador para CitaComite (Administrador, Funcionario de Bienestar)
class CitaComiteSerializer(serializers.ModelSerializer):
    aprendiz_nombre = serializers.CharField(source="aprendiz.nombre", read_only=True)
    aprendiz_apellido = serializers.CharField(source="aprendiz.apellido", read_only=True)
    otros_invitados_detalle = serializers.SerializerMethodField()

    class Meta:
        model = CitaComite
        fields = [
            "id",
            "aprendiz",
            "aprendiz_nombre",
            "aprendiz_apellido",
            "fecha_hora",
            "motivo",
            "otros_invitados",
            "otros_invitados_detalle",
            "estado",
            "creada_por",
            "fecha_creacion",
        ]
        read_only_fields = ["creada_por", "fecha_creacion"]

    def get_otros_invitados_detalle(self, obj):
        return [
            f"{usuario.nombre} {usuario.apellido}" for usuario in obj.otros_invitados.all()
        ]

    def validate_aprendiz(self, value):
        if value.rol.nombre_rol.lower() != "aprendiz":
            raise serializers.ValidationError("El usuario seleccionado no es un aprendiz.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["creada_por"] = request.user
        return super().create(validated_data)

#HU010 - Serializador para busqueda fichas y notificaciones (Instructor, Aprendiz)
class FichaSerializer(serializers.ModelSerializer):
    programa_nombre = serializers.CharField(source="programa.nombre", read_only=True)

    class Meta:
        model = Ficha
        fields = [
            "id",
            "numero_ficha",
            "programa",
            "programa_nombre",
            "jornada",
            "fecha_inicio",
            "fecha_fin",
        ]

class NotificacionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source="usuario.nombre", read_only=True)

    class Meta:
        model = Notificacion
        fields = [
            "id",
            "usuario",
            "usuario_nombre",
            "tipo",
            "titulo",
            "contenido",
            "leida",
            "fecha_creacion",
        ]
        read_only_fields = ["fecha_creacion"]
        

#HU010 - Serializador para asignacion de fichas (Instructor)

class FichaSerializer(serializers.ModelSerializer):
    programa_nombre = serializers.CharField(source="programa.nombre", read_only=True)

    class Meta:
        model = Ficha
        fields = ["id", "numero_ficha", "programa_nombre", "jornada", "fecha_inicio", "fecha_fin"]

class AsignacionFichaSerializer(serializers.ModelSerializer):
    ficha_detalle = FichaSerializer(source="ficha", read_only=True)
    instructor_nombre = serializers.CharField(source="instructor.nombre", read_only=True)

    class Meta:
        model = AsignacionFicha
        fields = [
            "id",
            "instructor",
            "instructor_nombre",
            "ficha",
            "ficha_detalle",
            "estado",
            "fecha_asignacion",
        ]
        
#HU012 - Serializador para Reporte Trimestral (Instructor)

class ReporteTrimestralSerializer(serializers.ModelSerializer):
    instructor_nombre = serializers.CharField(source="instructor.nombre", read_only=True)
    ficha_numero = serializers.CharField(source="ficha.numero_ficha", read_only=True)

    class Meta:
        model = ReporteTrimestral
        fields = [
            "id",
            "instructor",
            "instructor_nombre",
            "ficha",
            "ficha_numero",
            "archivo",
            "fecha_cargue",
            "observaciones",
        ]
        read_only_fields = ["fecha_cargue"]


class ActividadSerializer(serializers.ModelSerializer):
    instructor_nombre = serializers.CharField(source="instructor.nombre", read_only=True)
    aprendiz_nombre = serializers.CharField(source="aprendiz.nombre", read_only=True)

    class Meta:
        model = Actividad
        fields = [
            "id",
            "instructor",
            "instructor_nombre",
            "aprendiz",
            "aprendiz_nombre",
            "nombre",
            "descripcion",
            "nota",
            "estado",
            "fecha_limite",
            "plazo_extra",
            "observaciones",
            "etiqueta",
            "fecha_creacion",
        ]
        read_only_fields = ["estado", "fecha_creacion"]

    def create(self, validated_data):
        """
        Asigna automáticamente el instructor autenticado.
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["instructor"] = request.user
        return super().create(validated_data)

