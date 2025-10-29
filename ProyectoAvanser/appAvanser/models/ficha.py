from django.db import models
from programa_formacion import ProgramaFormacion
from usuario import Aprendiz, Instructor

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