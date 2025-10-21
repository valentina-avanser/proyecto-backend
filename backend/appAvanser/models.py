from django.contrib.auth.models import AbstractUser
from django.db import models


rol_choices = [
        ('aprendiz', 'Aprendiz'),
        ('funcionario', 'Funcionario'),
        ('instructor', 'Instructor'),
        ('coordinadorBienestar', 'Coordinador Bienestar'),
        ('coordinadorInstructores', 'Coordinador Instructores'),
    ]

class Usuario(AbstractUser):

    estado = models.BooleanField(default=True)
    documento = models.CharField(max_length=30, unique=True, null=True, blank=True)
    rol = models.CharField(max_length=50, choices=rol_choices)
    email = models.EmailField(unique=True) 
    
    # 👇 NUEVO: Para controlar el primer acceso
    primer_ingreso = models.BooleanField(default=True)
    debe_cambiar_password = models.BooleanField(default=True)
    roles_extra = models.JSONField(
        null=True, blank=True,
        help_text="Lista de roles adicionales si el usuario cumple más de una función (ej: ['instructor', 'coordinadorInstructores'])"
    )

    def tiene_rol(self, rol):
        """Verifica si el usuario tiene un rol principal o adicional"""
        return self.rol == rol or (self.roles_extra and rol in self.roles_extra)

    def __str__(self):
        return self.username
    



class Instructor(models.Model):
    instUsuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    especialidad = models.CharField(max_length=100)
    competencia = models.CharField(max_length=100, null=True, blank=True)
    es_coordinador = models.BooleanField(default=False)

    def __str__(self):
        return f"Instructor: {self.instUsuario.username}"

class Funcionario(models.Model):
    funcUsuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    cargo = models.CharField(max_length=50, default="Sin cargo")

    def __str__(self):
        return f"Funcionario: {self.funcUsuario.username}"

class CoordinadorBienestar(models.Model):
    coordBienestarUsuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    def __str__(self):
        return f"Coordinador Bienestar: {self.coordBienestarUsuario.username}"

class CoordinadorInstructores(models.Model):
    coordInstructoresUsuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    tambien_instructor = models.BooleanField(default=False)
    def __str__(self):
        return f"Coordinador Instructores: {self.coordInstructoresUsuario.username}"


class ProgramaFormacion(models.Model):
    nombre = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)
    duracion_meses = models.IntegerField()
    modalidad = models.CharField(max_length=50)
    fecha_inicio_programa = models.DateTimeField(null=True)
    fecha_fin_programa = models.DateTimeField(null=True)

    def __str__(self):
        return self.nombre


class Ficha(models.Model):
    numero_ficha = models.CharField(max_length=50, unique=True)
    programa = models.ForeignKey(ProgramaFormacion, on_delete=models.PROTECT)
    jornada = models.CharField(max_length=50)
    fecha_inicio = models.DateTimeField(null=True)
    fecha_fin = models.DateTimeField(null=True)

        # 👇 Un solo instructor líder por ficha
    instructor_lider = models.ForeignKey(
        'Instructor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas_lideradas'
    )

    # 👇 Varios instructores asociados (normales)
    instructores = models.ManyToManyField(
        'Instructor',
        related_name='fichas_asignadas',
        blank=True
    )

    def __str__(self):
        return f"{self.numero_ficha} - {self.programa.nombre}"



class Aprendiz(models.Model):
    apUsuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    ficha = models.ForeignKey(Ficha, on_delete=models.PROTECT, null=True, blank=True)
    estado = models.BooleanField(default=True)
    fecha_ingreso = models.DateTimeField(null=True)
    fecha_egreso = models.DateTimeField(blank=True, null=True)
    # 👇 NUEVOS CAMPOS: Datos temporales antes de crear usuario
    documento_temp = models.CharField(max_length=30, null=True, blank=True)
    nombres_temp = models.CharField(max_length=100, null=True, blank=True)
    apellidos_temp = models.CharField(max_length=100, null=True, blank=True)
    email_temp = models.EmailField(null=True, blank=True)
    telefono_temp = models.CharField(max_length=20, null=True, blank=True)
    
    # Para el registro
    usuario_creado = models.BooleanField(default=False)
    fecha_registro_caracterizacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.apUsuario:
            return f"{self.apUsuario.username} en {self.ficha.numero_ficha if self.ficha else 'Sin ficha'}"
        return f"Aprendiz temporal - {self.documento_temp}"


resultadoPostulacion = [
    ('Beneficiado','Beneficiado'),
    ('No Beneficiado','No Beneficiado')
]

class TipoConvocatoria(models.Model):
    tip_nombre = models.CharField(max_length=50, unique=True)    
     
    def __str__(self):
        return self.tip_nombre
    
class Convocatoria(models.Model):
    con_nombre = models.CharField(max_length=200)
    con_tipo = models.ForeignKey(TipoConvocatoria, on_delete=models.PROTECT)
    con_cantidad_beneficiarios = models.IntegerField()
    con_fecha_inicio = models.DateTimeField()
    con_fecha_final = models.DateTimeField()
    con_fecha_creacion = models.DateTimeField(auto_now_add=True)
    con_documento = models.FileField(upload_to='convocatorias/', blank=True, null=True)

    def __str__(self):
        return self.con_nombre

class Postulacion(models.Model):
    pos_aprendiz = models.ForeignKey(Aprendiz, on_delete=models.PROTECT)
    pos_convocatoria = models.ForeignKey(Convocatoria, on_delete=models.PROTECT)
    pos_fecha_hora_postulacion = models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return f"{self.pos_aprendiz}-{self.pos_convocatoria}"

class ResultadoPostulacion(models.Model):
    res_postulacion = models.ForeignKey(Postulacion, on_delete=models.PROTECT, related_name='resultados_postulacion')
    res_valoracion = models.IntegerField()
    res_resultado = models.CharField(max_length=16, choices=resultadoPostulacion, 
    null=True, default=None)
    res_fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.res_valoracion} {self.res_resultado}"

class Caracterizacion(models.Model):
    """
    Caracterización aplicada a aprendices por año y trimestre
    """
    id_aprendiz = models.ForeignKey(Aprendiz,on_delete=models.CASCADE,related_name='caracterizaciones', null=True,  # ← Ahora puede ser null
        blank=True
    )

    documento_solicitante = models.CharField(max_length=30, null=True, blank=True)
    email_solicitante = models.EmailField(null=True, blank=True)
    telefono_solicitante = models.CharField(max_length=20, null=True, blank=True)
    

    anio = models.IntegerField(help_text="Año de la caracterización (ej: 2024)")
    trimestre = models.CharField(
        max_length=2,
        choices=[
            ('T1', 'Trimestre 1'),
            ('T2', 'Trimestre 2'),
            ('T3', 'Trimestre 3'),
            ('T4', 'Trimestre 4'),
            ('T5', 'Trimestre 5'),
            ('T6', 'Trimestre 6'),
            ('T7', 'Trimestre 7'),
            ('T8', 'Trimestre 8'),
        ],
        help_text="Trimestre en el que se realiza"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    completada = models.BooleanField(default=False)

    # 👇 NUEVOS CAMPOS para el proceso de registro
    acepta_terminos = models.BooleanField(default=False)
    fecha_aceptacion_terminos = models.DateTimeField(null=True, blank=True)
    ip_registro = models.GenericIPAddressField(null=True, blank=True)
    usuario_creado_desde_caracterizacion = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Caracterización'
        verbose_name_plural = 'Caracterizaciones'
        ordering = ['-fecha_creacion']

    def __str__(self):
        if self.id_aprendiz:
            return f"Caracterización {self.anio}-{self.trimestre} - {self.id_aprendiz.apUsuario.username}"
        return f"Caracterización pública - {self.documento_solicitante}"

    def obtener_progreso(self):
        """Calcula el porcentaje de preguntas respondidas"""
        total_preguntas = self.preguntas.count()
        
        if total_preguntas == 0:
            return 0
        
        preguntas_respondidas = self.respuestas.filter(
            respuesta__isnull=False
        ).exclude(respuesta='').count()
        
        return int((preguntas_respondidas / total_preguntas) * 100)


class PreguntaCaracterizacion(models.Model):
    """
    Preguntas de la caracterización
    """
    TIPO_PREGUNTA_CHOICES = [
        ('texto', 'Texto Libre'),
        ('seleccion_simple', 'Selección Simple'),
        ('seleccion_multiple', 'Selección Múltiple'),
        ('si_no', 'Sí/No'),
        ('numero', 'Numérico'),
        ('fecha', 'Fecha'),
        ('escala', 'Escala (1-5)'),
    ]

    id_caracterizacion = models.ForeignKey(Caracterizacion,on_delete=models.CASCADE,related_name='preguntas')
    pregunta = models.TextField(help_text="Texto de la pregunta")
    tipo_pregunta = models.CharField(max_length=20,choices=TIPO_PREGUNTA_CHOICES,default='texto')
    obligatoria = models.BooleanField(default=False,help_text="Si es obligatoria, el aprendiz debe responderla")
    opciones = models.JSONField(null=True,blank=True,help_text="Opciones para preguntas de selección. Ej: ['Opción 1', 'Opción 2']")
    orden = models.IntegerField(default=0,help_text="Orden de aparición de la pregunta")

    class Meta:
        verbose_name = 'Pregunta de Caracterización'
        verbose_name_plural = 'Preguntas de Caracterización'
        ordering = ['orden', 'id']

    def __str__(self):
        return f"P{self.orden}: {self.pregunta[:50]}..."


class RespuestaCaracterizacion(models.Model):
    """
    Respuestas a las preguntas de caracterización
    """
    id_caracterizacion = models.ForeignKey(
        Caracterizacion,
        on_delete=models.CASCADE,
        related_name='respuestas'
    )
    id_pregunta = models.ForeignKey(
        PreguntaCaracterizacion,
        on_delete=models.CASCADE,
        related_name='respuestas'
    )
    respuesta = models.TextField(
        blank=True,
        null=True,
        help_text="Respuesta del aprendiz"
    )
    fecha_respuesta = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['id_caracterizacion', 'id_pregunta']
        verbose_name = 'Respuesta de Caracterización'
        verbose_name_plural = 'Respuestas de Caracterización'

    def __str__(self):
        respuesta_corta = self.respuesta[:50] if self.respuesta else "Sin respuesta"
        return f"{self.id_pregunta.pregunta[:30]}... → {respuesta_corta}"

    def clean(self):
        """Validación personalizada"""
        from django.core.exceptions import ValidationError
        
        # Verificar que la pregunta pertenece a la caracterización
        if self.id_pregunta.id_caracterizacion != self.id_caracterizacion:
            raise ValidationError(
                'La pregunta no pertenece a esta caracterización'
            )
        
        # Verificar que respuesta obligatoria no esté vacía
        if self.id_pregunta.obligatoria and not self.respuesta:
            raise ValidationError(
                f'La pregunta "{self.id_pregunta.pregunta}" es obligatoria'
            )

class PlantillaCaracterizacion(models.Model):
    """
    Plantilla base de preguntas para caracterización
    Se usa para generar las preguntas de cada caracterización
    """
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    activa = models.BooleanField(default=True)
    es_plantilla_inicial = models.BooleanField(
        default=False,
        help_text="Esta es la plantilla para nuevos registros"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Plantilla de Caracterización'
        verbose_name_plural = 'Plantillas de Caracterización'
    
    def __str__(self):
        return self.nombre

class PreguntaPlantilla(models.Model):
    """
    Preguntas de la plantilla base
    """
    TIPO_PREGUNTA_CHOICES = [
        ('texto', 'Texto Libre'),
        ('email', 'Correo Electrónico'),
        ('telefono', 'Teléfono'),
        ('documento', 'Número de Documento'),
        ('seleccion_simple', 'Selección Simple'),
        ('seleccion_multiple', 'Selección Múltiple'),
        ('si_no', 'Sí/No'),
        ('numero', 'Numérico'),
        ('fecha', 'Fecha'),
        ('escala', 'Escala (1-5)'),
    ]
    
    CATEGORIA_CHOICES = [
        ('datos_personales', 'Datos Personales'),
        ('datos_academicos', 'Datos Académicos'),
        ('datos_socioeconomicos', 'Datos Socioeconómicos'),
        ('datos_salud', 'Datos de Salud'),
        ('datos_bienestar', 'Datos de Bienestar'),
    ]
    
    plantilla = models.ForeignKey(
        PlantillaCaracterizacion,
        on_delete=models.CASCADE,
        related_name='preguntas_plantilla'
    )
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    pregunta = models.TextField()
    tipo_pregunta = models.CharField(max_length=20, choices=TIPO_PREGUNTA_CHOICES)
    obligatoria = models.BooleanField(default=False)
    opciones = models.JSONField(null=True, blank=True)
    orden = models.IntegerField(default=0)
    ayuda = models.TextField(blank=True, help_text="Texto de ayuda para la pregunta")
    
    # 👇 IMPORTANTE: Mapeo a campos del modelo
    campo_usuario = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Campo del modelo Usuario que se llena con esta respuesta (ej: 'first_name', 'email')"
    )
    campo_aprendiz = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Campo del modelo Aprendiz que se llena con esta respuesta"
    )
    
    class Meta:
        ordering = ['orden']
        verbose_name = 'Pregunta de Plantilla'
        verbose_name_plural = 'Preguntas de Plantilla'
    
    def __str__(self):
        return f"{self.orden}. {self.pregunta[:50]}..."