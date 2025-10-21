
# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Instructor, Funcionario, CoordinadorBienestar, CoordinadorInstructores,
    ProgramaFormacion, Ficha, Aprendiz, TipoConvocatoria, Convocatoria,
    Postulacion, ResultadoPostulacion, Caracterizacion, PreguntaCaracterizacion,
    RespuestaCaracterizacion
)


# ============================================
# USUARIO Y ROLES
# ============================================

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'documento', 'first_name', 'last_name', 'rol', 'estado']
    list_filter = ['rol', 'estado', 'is_staff', 'is_active']
    search_fields = ['username', 'documento', 'first_name', 'last_name', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('documento', 'rol', 'estado')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('documento', 'rol', 'estado')
        }),
    )


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['get_nombre', 'especialidad', 'get_usuario']
    search_fields = ['instUsuario__username', 'instUsuario__first_name', 'instUsuario__last_name', 'especialidad']
    list_filter = ['especialidad']
    
    def get_nombre(self, obj):
        return f"{obj.instUsuario.first_name} {obj.instUsuario.last_name}"
    get_nombre.short_description = 'Nombre'
    
    def get_usuario(self, obj):
        return obj.instUsuario.username
    get_usuario.short_description = 'Usuario'


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['get_nombre', 'cargo', 'get_usuario']
    search_fields = ['funcUsuario__username', 'funcUsuario__first_name', 'funcUsuario__last_name']
    list_filter = ['cargo']
    
    def get_nombre(self, obj):
        return f"{obj.funcUsuario.first_name} {obj.funcUsuario.last_name}"
    get_nombre.short_description = 'Nombre'
    
    def get_usuario(self, obj):
        return obj.funcUsuario.username
    get_usuario.short_description = 'Usuario'


@admin.register(CoordinadorBienestar)
class CoordinadorBienestarAdmin(admin.ModelAdmin):
    list_display = ['get_nombre', 'get_usuario']
    search_fields = ['coordBienestarUsuario__username', 'coordBienestarUsuario__first_name']
    
    def get_nombre(self, obj):
        return f"{obj.coordBienestarUsuario.first_name} {obj.coordBienestarUsuario.last_name}"
    get_nombre.short_description = 'Nombre'
    
    def get_usuario(self, obj):
        return obj.coordBienestarUsuario.username
    get_usuario.short_description = 'Usuario'


@admin.register(CoordinadorInstructores)
class CoordinadorInstructoresAdmin(admin.ModelAdmin):
    list_display = ['get_nombre', 'get_usuario']
    search_fields = ['coordInstructoresUsuario__username', 'coordInstructoresUsuario__first_name']
    
    def get_nombre(self, obj):
        return f"{obj.coordInstructoresUsuario.first_name} {obj.coordInstructoresUsuario.last_name}"
    get_nombre.short_description = 'Nombre'
    
    def get_usuario(self, obj):
        return obj.coordInstructoresUsuario.username
    get_usuario.short_description = 'Usuario'


# ============================================
# PROGRAMAS Y FICHAS
# ============================================

@admin.register(ProgramaFormacion)
class ProgramaFormacionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nivel', 'modalidad', 'duracion_meses', 'fecha_inicio_programa']
    list_filter = ['nivel', 'modalidad']
    search_fields = ['nombre']
    date_hierarchy = 'fecha_inicio_programa'


class InstructorInline(admin.TabularInline):
    model = Ficha.instructores.through
    extra = 1
    verbose_name = "Instructor Asignado"
    verbose_name_plural = "Instructores Asignados"


@admin.register(Ficha)
class FichaAdmin(admin.ModelAdmin):
    list_display = ['numero_ficha', 'programa', 'jornada', 'get_instructor_lider', 'fecha_inicio', 'get_total_aprendices']
    list_filter = ['jornada', 'programa']
    search_fields = ['numero_ficha', 'programa__nombre']
    date_hierarchy = 'fecha_inicio'
    filter_horizontal = ['instructores']
    
    inlines = []  # Puedes agregar InstructorInline si quieres
    
    def get_instructor_lider(self, obj):
        return obj.instructor_lider if obj.instructor_lider else "Sin líder"
    get_instructor_lider.short_description = 'Instructor Líder'
    
    def get_total_aprendices(self, obj):
        return obj.aprendiz_set.filter(estado=True).count()
    get_total_aprendices.short_description = 'Aprendices Activos'


# ============================================
# APRENDICES
# ============================================

@admin.register(Aprendiz)
class AprendizAdmin(admin.ModelAdmin):
    list_display = ['get_nombre', 'get_documento', 'ficha', 'estado', 'fecha_ingreso']
    list_filter = ['estado', 'ficha']
    search_fields = ['apUsuario__username', 'apUsuario__first_name', 'apUsuario__last_name', 'apUsuario__documento']
    date_hierarchy = 'fecha_ingreso'
    
    def get_nombre(self, obj):
        return f"{obj.apUsuario.first_name} {obj.apUsuario.last_name}"
    get_nombre.short_description = 'Nombre'
    
    def get_documento(self, obj):
        return obj.apUsuario.documento
    get_documento.short_description = 'Documento'


# ============================================
# CONVOCATORIAS
# ============================================

@admin.register(TipoConvocatoria)
class TipoConvocatoriaAdmin(admin.ModelAdmin):
    list_display = ['tip_nombre']
    search_fields = ['tip_nombre']


class PostulacionInline(admin.TabularInline):
    model = Postulacion
    extra = 0
    readonly_fields = ['pos_fecha_hora_postulacion']
    can_delete = False


@admin.register(Convocatoria)
class ConvocatoriaAdmin(admin.ModelAdmin):
    list_display = ['con_nombre', 'con_tipo', 'con_cantidad_beneficiarios', 'con_fecha_inicio', 'con_fecha_final', 'get_total_postulaciones']
    list_filter = ['con_tipo', 'con_fecha_creacion']
    search_fields = ['con_nombre']
    date_hierarchy = 'con_fecha_inicio'
    
    inlines = [PostulacionInline]
    
    def get_total_postulaciones(self, obj):
        # Evita el error si aún no existen postulaciones
        if not hasattr(obj, 'postulaciones'):
            return 0
        return obj.postulaciones.count()



@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ['get_aprendiz', 'pos_convocatoria', 'pos_fecha_hora_postulacion', 'get_resultado']
    list_filter = ['pos_convocatoria', 'pos_fecha_hora_postulacion']
    search_fields = ['pos_aprendiz__apUsuario__username', 'pos_convocatoria__con_nombre']
    date_hierarchy = 'pos_fecha_hora_postulacion'
    readonly_fields = ['pos_fecha_hora_postulacion']
    
    def get_aprendiz(self, obj):
        return f"{obj.pos_aprendiz.apUsuario.first_name} {obj.pos_aprendiz.apUsuario.last_name}"
    get_aprendiz.short_description = 'Aprendiz'
    
    def get_resultado(self, obj):
        resultado = obj.resultados_postulacion.first()
        return resultado.res_resultado if resultado else 'Pendiente'
    get_resultado.short_description = 'Resultado'


@admin.register(ResultadoPostulacion)
class ResultadoPostulacionAdmin(admin.ModelAdmin):
    list_display = ['get_aprendiz', 'get_convocatoria', 'res_valoracion', 'res_resultado', 'res_fecha_actualizacion']
    list_filter = ['res_resultado', 'res_fecha_actualizacion']
    search_fields = ['res_postulacion__pos_aprendiz__apUsuario__username']
    date_hierarchy = 'res_fecha_actualizacion'
    
    def get_aprendiz(self, obj):
        return f"{obj.res_postulacion.pos_aprendiz.apUsuario.first_name} {obj.res_postulacion.pos_aprendiz.apUsuario.last_name}"
    get_aprendiz.short_description = 'Aprendiz'
    
    def get_convocatoria(self, obj):
        return obj.res_postulacion.pos_convocatoria.con_nombre
    get_convocatoria.short_description = 'Convocatoria'


# ============================================
# CARACTERIZACIÓN
# ============================================

class PreguntaCaracterizacionInline(admin.TabularInline):
    model = PreguntaCaracterizacion
    extra = 1
    fields = ['orden', 'pregunta', 'tipo_pregunta', 'obligatoria', 'opciones']
    ordering = ['orden']


class RespuestaCaracterizacionInline(admin.TabularInline):
    model = RespuestaCaracterizacion
    extra = 0
    readonly_fields = ['id_pregunta', 'fecha_respuesta']
    fields = ['id_pregunta', 'respuesta', 'fecha_respuesta']
    can_delete = False


@admin.register(Caracterizacion)
class CaracterizacionAdmin(admin.ModelAdmin):
    list_display = ['get_aprendiz', 'anio', 'trimestre', 'completada', 'get_progreso', 'fecha_actualizacion']
    list_filter = ['anio', 'trimestre', 'completada', 'id_aprendiz__ficha']
    search_fields = ['id_aprendiz__apUsuario__username', 'id_aprendiz__apUsuario__first_name', 'id_aprendiz__apUsuario__last_name']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'get_progreso']
    
    inlines = [PreguntaCaracterizacionInline, RespuestaCaracterizacionInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id_aprendiz', 'anio', 'trimestre', 'completada')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion', 'get_progreso'),
            'classes': ('collapse',)
        }),
    )
    def get_aprendiz(self, obj):
        if not obj.id_aprendiz:
            return "Sin aprendiz asignado"
        aprendiz = obj.id_aprendiz
        usuario = aprendiz.apUsuario
        nombre = f"{usuario.first_name} {usuario.last_name}"
        ficha = aprendiz.ficha.numero_ficha if aprendiz.ficha else "Sin ficha"
        return f"{nombre} ({ficha})"

    get_aprendiz.short_description = 'Aprendiz'

    
    def get_progreso(self, obj):
        progreso = obj.obtener_progreso()
        return f"{progreso}%"
    get_progreso.short_description = 'Progreso'
    
    actions = ['marcar_como_completada', 'marcar_como_incompleta']
    
    def marcar_como_completada(self, request, queryset):
        updated = queryset.update(completada=True)
        self.message_user(request, f"{updated} caracterización(es) marcada(s) como completada(s).")
    marcar_como_completada.short_description = "Marcar como completada"
    
    def marcar_como_incompleta(self, request, queryset):
        updated = queryset.update(completada=False)
        self.message_user(request, f"{updated} caracterización(es) marcada(s) como incompleta(s).")
    marcar_como_incompleta.short_description = "Marcar como incompleta"


@admin.register(PreguntaCaracterizacion)
class PreguntaCaracterizacionAdmin(admin.ModelAdmin):
    list_display = ['orden', 'get_pregunta_corta', 'tipo_pregunta', 'obligatoria', 'get_caracterizacion']
    list_filter = ['tipo_pregunta', 'obligatoria', 'id_caracterizacion__anio', 'id_caracterizacion__trimestre']
    search_fields = ['pregunta', 'id_caracterizacion__id_aprendiz__apUsuario__username']
    ordering = ['id_caracterizacion', 'orden']
    
    def get_pregunta_corta(self, obj):
        return obj.pregunta[:50] + '...' if len(obj.pregunta) > 50 else obj.pregunta
    get_pregunta_corta.short_description = 'Pregunta'
    
    def get_caracterizacion(self, obj):
        return f"{obj.id_caracterizacion.id_aprendiz.apUsuario.username} - {obj.id_caracterizacion.anio}/{obj.id_caracterizacion.trimestre}"
    get_caracterizacion.short_description = 'Caracterización'


@admin.register(RespuestaCaracterizacion)
class RespuestaCaracterizacionAdmin(admin.ModelAdmin):
    list_display = ['get_aprendiz', 'get_pregunta_corta', 'get_respuesta_corta', 'fecha_respuesta']
    list_filter = ['fecha_respuesta', 'id_caracterizacion__anio', 'id_caracterizacion__trimestre']
    search_fields = [
        'id_caracterizacion__id_aprendiz__apUsuario__username',
        'id_pregunta__pregunta',
        'respuesta'
    ]
    date_hierarchy = 'fecha_respuesta'
    readonly_fields = ['fecha_respuesta']
    
    def get_aprendiz(self, obj):
        return f"{obj.id_caracterizacion.id_aprendiz.apUsuario.first_name} {obj.id_caracterizacion.id_aprendiz.apUsuario.last_name}"
    get_aprendiz.short_description = 'Aprendiz'
    
    def get_pregunta_corta(self, obj):
        return obj.id_pregunta.pregunta[:40] + '...' if len(obj.id_pregunta.pregunta) > 40 else obj.id_pregunta.pregunta
    get_pregunta_corta.short_description = 'Pregunta'
    
    def get_respuesta_corta(self, obj):
        if not obj.respuesta:
            return "Sin respuesta"
        return obj.respuesta[:50] + '...' if len(obj.respuesta) > 50 else obj.respuesta
    get_respuesta_corta.short_description = 'Respuesta'


# ============================================
# PERSONALIZACIÓN DEL ADMIN
# ============================================

admin.site.site_header = "Administración SENA - Bienestar y Formación"
admin.site.site_title = "Admin SENA"
admin.site.index_title = "Panel de Administración"