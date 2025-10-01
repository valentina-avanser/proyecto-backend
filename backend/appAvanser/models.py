from django.db import models


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
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)


class Aprendiz(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)


class FuncionarioBienestar(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    componente = models.CharField(max_length=100)


class Instructor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
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
    programa = models.ForeignKey(ProgramaFormacion, on_delete=models.CASCADE)
    jornada = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.numero_ficha


class AprendizFicha(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE)
    ficha = models.ForeignKey(Ficha, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20)
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField(blank=True, null=True)


class SesionClase(models.Model):
    ficha = models.ForeignKey(Ficha, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    qr_codigo = models.CharField(max_length=255, blank=True, null=True)


class Asistencia(models.Model):
    sesion = models.ForeignKey(SesionClase, on_delete=models.CASCADE)
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE)
    fecha_hora_registro = models.DateTimeField()
    estado = models.CharField(max_length=20)


class Reporte(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    contenido = models.TextField()
    generado_por = models.CharField(max_length=100)


class ReporteAcademico(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    fecha = models.DateTimeField()


# ------------------------
# CARACTERIZACIÓN Y ENCUESTAS
# ------------------------
class Caracterizacion(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE)
    anio = models.IntegerField()
    trimestre = models.SmallIntegerField()


class PreguntaCaracterizacion(models.Model):
    caracterizacion = models.ForeignKey(Caracterizacion, on_delete=models.CASCADE)
    tipo_pregunta = models.CharField(max_length=50)
    obligatoria = models.BooleanField(default=False)
    pregunta = models.TextField()


class RespuestaCaracterizacion(models.Model):
    pregunta = models.ForeignKey(PreguntaCaracterizacion, on_delete=models.CASCADE)
    respuesta = models.TextField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)


class EncuestaAprendiz(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()


class PreguntaEncuesta(models.Model):
    encuesta = models.ForeignKey(EncuestaAprendiz, on_delete=models.CASCADE)
    texto = models.TextField()
    tipo = models.CharField(max_length=50)


class RespuestaEncuesta(models.Model):
    pregunta = models.ForeignKey(PreguntaEncuesta, on_delete=models.CASCADE)
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE)
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
    tipo_convocatoria = models.ForeignKey(TipoConvocatoria, on_delete=models.CASCADE)


class Postulacion(models.Model):
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE)
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)


class ResultadoPostulacion(models.Model):
    postulacion = models.ForeignKey(Postulacion, on_delete=models.CASCADE)
    resultado = models.CharField(max_length=50)
    valoracion = models.CharField(max_length=100, blank=True, null=True)
    fecha_update = models.DateTimeField(auto_now=True)


# ------------------------
# OTROS
# ------------------------
class ConsentimientoComunicacion(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE)
    medio = models.CharField(max_length=50)
    aceptado = models.BooleanField()
    fecha = models.DateTimeField(auto_now_add=True)


class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=50)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20)


class Riesgo(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    nivel = models.CharField(max_length=50)
    generado_por = models.CharField(max_length=100)
