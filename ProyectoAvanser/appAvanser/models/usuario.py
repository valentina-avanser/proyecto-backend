from django.db import models
from datetime import date
from rol import Rol

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
