from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_name="app_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="app_user_permissions",
        related_query_name="user",
    )
    



class Aprendiz(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT, related_name="perfil_aprendiz")

    def __str__(self):
        return f"Aprendiz: {self.usuario.username}"
    
class Instructor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return f"Instructor: {self.usuario.username}"


class FuncionarioBienestar(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    componente = models.CharField(max_length=100)

    def __str__(self):
        return f"Funcionario Bienestar: {self.usuario.username}"


class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)

    def __str__(self):
        return f"Administrador: {self.usuario.username}"
    

class ProgramaFormacion(models.Model):
    nombre = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)
    duracion_meses = models.IntegerField()
    modalidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Ficha(models.Model):
    numero_ficha = models.CharField(max_length=50, unique=True)
    programa = models.ForeignKey(ProgramaFormacion, on_delete=models.PROTECT)
    jornada = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"Ficha {self.numero_ficha} - {self.programa.nombre}"


class AprendizFicha(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.PROTECT)
    ficha = models.ForeignKey(Ficha, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20)
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.aprendiz.usuario.username} en {self.ficha.numero_ficha}"
    
class ReporteAcademico(models.Model):
    aprendiz = models.ForeignKey(Aprendiz, on_delete=models.PROTECT)
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    fecha = models.DateField()
    
class Competencia(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

class Horario(models.Model):
    descripcion = models.CharField(max_length=255)
    def __str__(self):
            return self.descripcion
    
class FichaCompetencia(models.Model):
    ficha = models.ForeignKey('Ficha', on_delete=models.CASCADE)
    competencia = models.ForeignKey('Competencia', on_delete=models.CASCADE)
    
    class Meta:
         unique_together = ('ficha', 'competencia')
    
    def __str__(self):
        return f"Ficha {self.ficha.numero_ficha} - Comp: {self.competencia.nombre}"

class FichaHorario(models.Model):
    ficha = models.ForeignKey('Ficha', on_delete=models.CASCADE)
    horario = models.ForeignKey('Horario', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('ficha', 'horario') 

    def __str__(self):
        return f"Ficha {self.ficha.numero_ficha} - Horario ID: {self.horario.id}"