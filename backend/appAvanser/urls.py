from django import views
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_aprendiz import *
from .views import *
from appAvanser import views_aprendiz
from . import views


urlpatterns = [
    # ============================================
    # RUTAS PÚBLICAS (Sin login)
    # ============================================
    path('', views_aprendiz.landing_page, name='landing_page'),
    path('login/', views_aprendiz.login_view, name='login'),
    path('logout/', views_aprendiz.logout_view, name='logout'),
    
    # Proceso de caracterización (registro de aprendices)
    path('iniciar/', views_aprendiz.iniciar_caracterizacion, name='iniciar_caracterizacion'),
    path('formulario/<int:pk>/', views_aprendiz.formulario_caracterizacion, name='formulario_caracterizacion'),
    path('registro-completado/', views_aprendiz.registro_completado, name='registro_completado'),
    
    # ============================================
    # RUTAS CON LOGIN - APRENDICES
    # ============================================
    path('cambiar-password/', views_aprendiz.cambiar_password_inicial, name='cambiar_password_inicial'),
    
    # ============================================
    # RUTAS CON LOGIN - COORDINADOR DE INSTRUCTORES
    # ============================================
        # Panel coordinador instructores
    path('panel_coordinador_instructores/', panel_coordinador_instructores, name='panel_coordinador_instructores'),
    
    # Endpoint para cargar instructores desde JSON
    path('cargar_instructores/', views.cargar_instructores, name='cargar_instructores'),
    
    # API REST de instructores
 



 
    
    # ============================================
    # RUTAS CON LOGIN - COORDINADOR DE BIENESTAR
    # ============================================
    path('coordinador-bienestar/', views_aprendiz.panel_coordinador_bienestar, name='panel_coordinador_bienestar'),
    
    # ============================================
    # RUTAS CON LOGIN - INSTRUCTOR
    # ============================================
    path('instructor/', views_aprendiz.panel_instructor, name='panel_instructor'),
    
    # ============================================
    # RUTAS CON LOGIN - FUNCIONARIO
    # ============================================
    path('funcionario/', views_aprendiz.panel_funcionario, name='panel_funcionario'),
    
    # ============================================
    # RUTAS CON LOGIN - DASHBOARD GENERAL
    # ============================================
    path('dashboard/', views_aprendiz.dashboard, name='dashboard'),
    
     # ============================================
    # API REST - USUARIOS Y ROLES
    # ============================================
    path('usuario/', UsuarioList.as_view()),
    path('usuario/<int:pk>/', UsuarioDetail.as_view(), name='usuario-detail'),
    path('aprendiz-usuario/', AprendizList.as_view()),
    path('aprendiz-usuario/<int:pk>/', AprendizDetail.as_view(), name='aprendiz-usuario-detail'),
    path('funcionario/', FuncionarioList.as_view()),
    path('funcionario/<int:pk>/', FuncionarioDetail.as_view(), name='funcionario-detail'),
    path('instructor/', InstructorList.as_view()),
    path('instructor/<int:pk>/', InstructorDetail.as_view(), name='instructor-detail'),
    
    # ============================================
    # API REST - PROGRAMAS Y FICHAS
    # ============================================
    path('programa/', ProgramaFormacionList.as_view()),
    path('programa/<int:pk>/', ProgramaFormacionDetail.as_view(), name='programa-detail'),
    path('ficha/', FichaList.as_view()),    
    path('ficha/<int:pk>/', FichaDetail.as_view(), name='ficha-detail'),
    
    # ============================================
    # API REST - CONVOCATORIAS
    # ============================================
    path('tipo-convocatoria/', TipoConvocatoriaList.as_view()),
    path('tipo-convocatoria/<int:pk>/', TipoConvocatoriaDetail.as_view(), name='tipo-convocatoria-detail'),
    path('convocatoria/', ConvocatoriaList.as_view()),
    path('convocatoria/<int:pk>/', ConvocatoriaDetail.as_view(), name='convocatoria-detail'),
    path('postulacion/', PostulacionList.as_view()),
    path('postulacion/<int:pk>/', PostulacionDetail.as_view(), name='postulacion-detail'),
    path('resultado-postulacion/', ResultadoPostulacionList.as_view()),
    path('resultado-postulacion/<int:pk>/', ResultadoPostulacionDetail.as_view(), name='resultado-postulacion-detail'),
]