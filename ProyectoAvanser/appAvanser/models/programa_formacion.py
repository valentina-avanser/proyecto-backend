from django.db import models


class ProgramaFormacion(models.Model):
    nombre = models.CharField(max_length=100)
    nivel = models.CharField(max_length=50)
    duracion_meses = models.PositiveSmallIntegerField()
    modalidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre