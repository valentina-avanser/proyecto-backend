
from django.contrib import admin

# Register your models here.

from .models import Usuario, Rol, Aprendiz, Instructor, Ficha, AprendizFicha, Convocatoria, CitaComite, ProgramaFormacion, TipoConvocatoria, Notificacion, AsignacionFicha, ReporteTrimestral, Actividad, Notificacion

admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(Aprendiz)
admin.site.register(Instructor)
admin.site.register(Ficha)
admin.site.register(AprendizFicha)  # para ver la relación aprendiz-ficha
admin.site.register(Convocatoria)
admin.site.register(ProgramaFormacion)
admin.site.register(TipoConvocatoria) # HU-08

# Admin personalizado para CitaComite y AsignacionFicha HU-08
@admin.register(CitaComite)
class CitaComiteAdmin(admin.ModelAdmin):
    list_display = ("aprendiz", "fecha_hora", "estado", "creada_por", "fecha_creacion")
    list_filter = ("estado", "fecha_hora")
    search_fields = ("aprendiz__username", "motivo")
    
# Admin personalizado para AsignacionFicha HU-10
@admin.register(AsignacionFicha)
class AsignacionFichaAdmin(admin.ModelAdmin):
    list_display = ("instructor", "ficha", "estado", "fecha_asignacion")
    list_filter = ("estado",)
    search_fields = ("instructor__nombre", "ficha__numero_ficha")
    
# 10
@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "usuario", "tipo", "leida", "fecha_creacion")
    list_filter = ("tipo", "leida")
    search_fields = ("titulo", "contenido", "usuario__nombre")

#HU012 - Registro de ReporteTrimestral y Actividad

@admin.register(ReporteTrimestral)
class ReporteTrimestralAdmin(admin.ModelAdmin):
    list_display = ("ficha", "instructor", "fecha_cargue")
    search_fields = ("ficha__numero_ficha", "instructor__nombre")

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "aprendiz", "nota", "estado", "fecha_limite", "plazo_extra")
    list_filter = ("estado", "plazo_extra")
    search_fields = ("nombre", "aprendiz__nombre")
