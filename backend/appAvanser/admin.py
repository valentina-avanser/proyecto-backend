from django.contrib import admin

# Register your models here.

from .models import Usuario, Rol, Aprendiz, Instructor, Ficha, Convocatoria

admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(Aprendiz)
admin.site.register(Instructor)
admin.site.register(Ficha)
admin.site.register(Convocatoria)
