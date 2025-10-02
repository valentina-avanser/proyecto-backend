from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    tipo_documento_choices = [
        ('CC', 'Cédula de ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('CE', 'Cédula de extranjería'),
        ('PA', 'Pasaporte'),
    ]

    rol_choices = [
        ('aprendiz', 'Aprendiz'),
        ('instructor', 'Instructor'),
        ('coordinador', 'Coordinador'),
        ('bienestar', 'Bienestar'),
    ]

    estado = models.BooleanField(default=True)
    tipo_documento = models.CharField(max_length=2, choices=tipo_documento_choices, null=True, blank=True)
    documento = models.CharField(max_length=30, unique=True, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=rol_choices, default='aprendiz')

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
    



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