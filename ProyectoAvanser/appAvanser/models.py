from django.db import models
from datetime import date

# ------------------------
# ROLES Y USUARIOS
# ------------------------
class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_rol


class Usuario(models.Model):
    TIPO_DOCUMENTO = [
        ('CC', 'Cédula de ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('CE', 'Cédula de extranjería'),
        ('PP', 'Pasaporte'),
        ('RC', 'Registro civil'),
    ]

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO)
    documento = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(unique=True, max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    contrasenia = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"


# ------------------------
# PERFILES
# ------------------------
class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)


class Aprendiz(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)


class FuncionarioBienestar(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    componente = models.CharField(max_length=100)


class Instructor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    especialidad = models.CharField(max_length=100)


# ------------------------
# ACADÉMICO
# ------------------------
class ProgramaFormacion(models.Model):
    nombre = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)
    duracion_meses = models.PositiveSmallIntegerField()
    modalidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Ficha(models.Model):
    numero_ficha = models.CharField(max_length=20, unique=True)
    programa = models.ForeignKey(ProgramaFormacion, on_delete=models.PROTECT)
    jornada = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.numero_ficha


class AprendizFicha(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.PROTECT)
    ficha = models.ForeignKey(Ficha, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20)
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField(blank=True, null=True)


class SesionClase(models.Model):
    ficha = models.ForeignKey(Ficha, on_delete=models.PROTECT)
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    fecha = models.DateField()
    estado = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    qr_codigo = models.CharField(max_length=255, blank=True, null=True)


class Asistencia(models.Model):
    sesion = models.ForeignKey(SesionClase, on_delete=models.PROTECT)
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.PROTECT)
    fecha_hora_registro = models.DateTimeField()
    estado = models.CharField(max_length=20)


class Reporte(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.PROTECT)
    fecha = models.DateTimeField()
    contenido = models.TextField()
    generado_por = models.CharField(max_length=100)


class ReporteAcademico(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.PROTECT)
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    fecha = models.DateTimeField()


# ------------------------
# CARACTERIZACIÓN Y ENCUESTAS
# ------------------------
class Caracterizacion(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.PROTECT)
    anio = models.IntegerField()
    trimestre = models.SmallIntegerField()


class PreguntaCaracterizacion(models.Model):
    caracterizacion = models.ForeignKey(Caracterizacion, on_delete=models.PROTECT)
    tipo_pregunta = models.CharField(max_length=50)
    obligatoria = models.BooleanField(default=False)
    pregunta = models.TextField()


class RespuestaCaracterizacion(models.Model):
    pregunta = models.ForeignKey(PreguntaCaracterizacion, on_delete=models.PROTECT)
    respuesta = models.TextField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)


class EncuestaAprendiz(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()


class PreguntaEncuesta(models.Model):
    encuesta = models.ForeignKey(EncuestaAprendiz, on_delete=models.PROTECT)
    texto = models.TextField()
    tipo = models.CharField(max_length=50)


class RespuestaEncuesta(models.Model):
    pregunta = models.ForeignKey(PreguntaEncuesta, on_delete=models.PROTECT)
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.PROTECT)
    respuesta = models.TextField()
    fecha_respuesta = models.DateTimeField()


# ------------------------
# CONVOCATORIAS Y POSTULACIONES
# ------------------------
class TipoConvocatoria(models.Model):
    tipo_nombre = models.CharField(max_length=100)


class Convocatoria(models.Model):
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    cant_beneficiarios = models.IntegerField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    documento = models.CharField(max_length=255, blank=True, null=True)
    tipo_convocatoria = models.ForeignKey(TipoConvocatoria, on_delete=models.PROTECT)


class Postulacion(models.Model):
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.PROTECT)
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.PROTECT)
    fecha_hora = models.DateTimeField(auto_now_add=True)


class ResultadoPostulacion(models.Model):
    postulacion = models.ForeignKey(Postulacion, on_delete=models.PROTECT)
    resultado = models.CharField(max_length=50)
    valoracion = models.CharField(max_length=100, blank=True, null=True)
    fecha_update = models.DateTimeField(auto_now=True)


# ------------------------
# OTROS
# ------------------------
class ConsentimientoComunicacion(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.PROTECT)
    medio = models.CharField(max_length=50)
    aceptado = models.BooleanField()
    fecha = models.DateTimeField(auto_now_add=True)

class Riesgo(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    nivel = models.CharField(max_length=50)
    generado_por = models.CharField(max_length=100)

#CITA COMITE HU008
class CitaComite(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("realizada", "Realizada"),
        ("cancelada", "Cancelada"),
    ]

    aprendiz = models.ForeignKey(
        "Usuario",
        on_delete=models.CASCADE,
        related_name="citas_comite"
    )
    fecha_hora = models.DateTimeField()
    motivo = models.TextField()
    otros_invitados = models.ManyToManyField(
        "Usuario",
        related_name="citas_invitado",
        blank=True
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    creada_por = models.ForeignKey(
        "Usuario",
        on_delete=models.SET_NULL,
        null=True,
        related_name="citas_creadas"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cita de {self.aprendiz.nombre} {self.aprendiz.apellido} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"

#HU010
class AsignacionFicha(models.Model):
    ESTADO_FICHA = [
        ("activa", "Activa"),
        ("deshabilitada", "Deshabilitada"),
    ]

    instructor = models.ForeignKey(
        "Usuario",
        on_delete=models.PROTECT,
        related_name="fichas_asignadas"
    )
    ficha = models.ForeignKey(
        "Ficha",
        on_delete=models.PROTECT,
        related_name="asignaciones"
    )
    estado = models.CharField(max_length=20, choices=ESTADO_FICHA, default="activa")
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("instructor", "ficha")

    def __str__(self):
        return f"{self.instructor.nombre} - {self.ficha.numero_ficha} ({self.estado})"
    
#HU010 Notificaciones
class Notificacion(models.Model):
    TIPOS = [
        ("alerta", "Alerta"),
        ("recordatorio", "Recordatorio"),
        ("mensaje", "Mensaje"),
        ("info", "Información"),
    ]

    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE, related_name="notificaciones")
    tipo = models.CharField(max_length=20, choices=TIPOS, default="mensaje")
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} → {self.usuario.nombre}"

    class Meta:
        ordering = ["-fecha_creacion"]
        

#HU012 Reporte Trimestral

class ReporteTrimestral(models.Model):
    instructor = models.ForeignKey("Usuario", on_delete=models.PROTECT, related_name="reportes_subidos")
    ficha = models.ForeignKey("Ficha", on_delete=models.PROTECT, related_name="reportes_trimestrales")
    archivo = models.FileField(upload_to="reportes/", null=True, blank=True)
    fecha_cargue = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reporte {self.ficha.numero_ficha} - {self.instructor.nombre}"

    class Meta:
        verbose_name = "Reporte Trimestral"
        verbose_name_plural = "Reportes Trimestrales"


class Actividad(models.Model):
    ESTADOS = [
        ("sin_revisar", "Sin revisar"),
        ("aprobado", "Aprobado"),
        ("aun_no_aprobado", "Aún no aprobado"),
        ("no_aprobado", "No aprobado"),
    ]

    instructor = models.ForeignKey("Usuario", on_delete=models.PROTECT, related_name="actividades_creadas")
    aprendiz = models.ForeignKey("Usuario", on_delete=models.PROTECT, related_name="actividades_asignadas")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    nota = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="sin_revisar")
    fecha_limite = models.DateField(null=True, blank=True)
    plazo_extra = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, null=True)
    etiqueta = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.aprendiz.nombre}"

    def save(self, *args, **kwargs):
        """
        Asigna automáticamente el estado según la nota y la fecha límite.
        """
        hoy = date.today()
        if self.nota is not None:
            if self.nota < 3:
                if self.fecha_limite and hoy > self.fecha_limite:
                    self.estado = "no_aprobado"
                else:
                    self.estado = "aun_no_aprobado"
            else:
                self.estado = "aprobado"
        super().save(*args, **kwargs)
