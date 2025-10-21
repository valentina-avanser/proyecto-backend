from urllib import request
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import secrets
import string
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .views import *
from django.utils.decorators import method_decorator


class UsuarioList(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioDetail(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class AprendizList(generics.ListCreateAPIView):
    queryset = Aprendiz.objects.all()
    serializer_class = AprendizSerializer
    permission_classes = [AllowAny]

class AprendizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Aprendiz.objects.all()
    serializer_class = AprendizSerializer

class FuncionarioList(generics.ListCreateAPIView):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [AllowAny]

class FuncionarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

class InstructorList(generics.ListCreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [AllowAny]  # ✅ Permite crear sin autenticación en API

    def create(self, request, *args, **kwargs):
        """
        Crea un instructor junto con su usuario
        """
        try:
            with transaction.atomic():
                # Extraer datos del request
                data = request.data
                usuario_data = data.get('instUsuario', {})
                
                # Campos obligatorios
                documento = usuario_data.get('documento', '').strip()
                username = usuario_data.get('username', '').strip()
                email = usuario_data.get('email', '').strip()
                first_name = usuario_data.get('first_name', '').strip()
                last_name = usuario_data.get('last_name', '').strip()
                
                especialidad = data.get('especialidad', 'No especificada')
                competencia = data.get('competencia', '')
                
                # Validaciones
                if not all([documento, username, email, first_name, last_name]):
                    return Response(
                        {'error': 'Faltan campos obligatorios: documento, username, email, first_name, last_name'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Verificar si ya existe el usuario
                if Usuario.objects.filter(documento=documento).exists():
                    return Response(
                        {'error': f'Ya existe un usuario con el documento {documento}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if Usuario.objects.filter(username=username).exists():
                    return Response(
                        {'error': f'Ya existe un usuario con el username {username}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if Usuario.objects.filter(email=email).exists():
                    return Response(
                        {'error': f'Ya existe un usuario con el email {email}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Crear usuario
                usuario = Usuario.objects.create(
                    username=username,
                    documento=documento,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    rol='instructor',
                    password=make_password(documento),  # Contraseña temporal = documento
                    debe_cambiar_password=True,
                    estado=True
                )
                
                # Crear instructor
                instructor = Instructor.objects.create(
                    instUsuario=usuario,
                    especialidad=especialidad,
                    competencia=competencia
                )
                
                # Serializar respuesta
                serializer = self.get_serializer(instructor)
                
                return Response(
                    {
                        'mensaje': 'Instructor creado exitosamente',
                        'data': serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
                
        except Exception as e:
            return Response(
                {'error': f'Error al crear instructor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        """
        Lista todos los instructores con sus datos de usuario
        """
        queryset = self.get_queryset().select_related('instUsuario')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class InstructorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [AllowAny]

    def update(self, request, *args, **kwargs):
        """
        Actualiza un instructor y su usuario
        """
        try:
            with transaction.atomic():
                instructor = self.get_object()
                data = request.data
                
                # Actualizar datos del usuario si vienen
                usuario_data = data.get('instUsuario', {})
                if usuario_data:
                    usuario = instructor.instUsuario
                    
                    if 'first_name' in usuario_data:
                        usuario.first_name = usuario_data['first_name']
                    if 'last_name' in usuario_data:
                        usuario.last_name = usuario_data['last_name']
                    if 'email' in usuario_data:
                        # Verificar que el email no esté en uso por otro usuario
                        if Usuario.objects.filter(email=usuario_data['email']).exclude(id=usuario.id).exists():
                            return Response(
                                {'error': 'El email ya está en uso por otro usuario'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        usuario.email = usuario_data['email']
                    
                    usuario.save()
                
                # Actualizar datos del instructor
                if 'especialidad' in data:
                    instructor.especialidad = data['especialidad']
                if 'competencia' in data:
                    instructor.competencia = data['competencia']
                
                instructor.save()
                
                serializer = self.get_serializer(instructor)
                return Response(
                    {
                        'mensaje': 'Instructor actualizado exitosamente',
                        'data': serializer.data
                    }
                )
                
        except Exception as e:
            return Response(
                {'error': f'Error al actualizar instructor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProgramaFormacionList(generics.ListCreateAPIView):
    queryset = ProgramaFormacion.objects.all()
    serializer_class = ProgramaFormacionSerializer
    permission_classes = [AllowAny]

class ProgramaFormacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProgramaFormacion.objects.all()
    serializer_class = ProgramaFormacionSerializer
    permission_classes = [AllowAny]

class FichaList(generics.ListCreateAPIView):
    queryset = Ficha.objects.all()
    serializer_class = FichaSerializer
    permission_classes = [AllowAny]     

class FichaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ficha.objects.all()
    serializer_class = FichaSerializer
    permission_classes = [AllowAny]

class CoordinadorBienestarList(generics.ListCreateAPIView):
    queryset = CoordinadorBienestar.objects.all()
    serializer_class = CoordinadorBienestarSerializer
    permission_classes = [AllowAny]

class CoordinadorBienestarDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CoordinadorBienestar.objects.all()
    serializer_class = CoordinadorBienestarSerializer
    permission_classes = [AllowAny]

class CoordinadorInstructoresList(generics.ListCreateAPIView):
    queryset = CoordinadorInstructores.objects.all()
    serializer_class = CoordinadorInstructoresSerializer
    permission_classes = [AllowAny]
    
class CoordinadorInstructoresDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CoordinadorInstructores.objects.all()
    serializer_class = CoordinadorInstructoresSerializer
    permission_classes = [AllowAny]

class TipoConvocatoriaList(generics.ListCreateAPIView):
    queryset = TipoConvocatoria.objects.all()
    serializer_class = TipoConvocatoriaSerializer
    permission_classes = [AllowAny]

class TipoConvocatoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TipoConvocatoria.objects.all()
    serializer_class = TipoConvocatoriaSerializer
    permission_classes = [AllowAny]

class ConvocatoriaList(generics.ListCreateAPIView):
    queryset = Convocatoria.objects.all()
    serializer_class = ConvocatoriaSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print(request.FILES) 
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {
                    'mensaje': 'Convocatoria creada correctamente',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'mensaje': 'Error al guardar el registro',
                    'errores': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ConvocatoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Convocatoria.objects.all()
    serializer_class = ConvocatoriaSerializer


class PostulacionList(generics.ListCreateAPIView):
    queryset = Postulacion.objects.all()
    serializer_class = PostulacionSerializer
    permission_classes = [AllowAny] 

class PostulacionDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Postulacion.objects.all()
    serializer_class = PostulacionSerializer
    permission_classes = [AllowAny]

class ResultadoPostulacionList(generics.ListCreateAPIView):
    queryset = ResultadoPostulacion.objects.all()
    serializer_class = ResultadoPostulacionSerializer
    permission_classes = [AllowAny]

class ResultadoPostulacionDetail(generics.RetrieveUpdateDestroyAPIView):    
    queryset = ResultadoPostulacion.objects.all()
    serializer_class = ResultadoPostulacionSerializer
    permission_classes = [AllowAny]




# ============================================
# FUNCIONES AUXILIARES
# ============================================

def obtener_cliente_ip(request):
    """Obtiene la IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generar_password_temporal():
    """Genera una contraseña temporal segura"""
    caracteres = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(caracteres) for _ in range(8))
    return password


def enviar_credenciales_correo(email, documento, password, nombre_completo):
    """Envía las credenciales de acceso por correo"""
    asunto = '🎓 Bienvenido a SENA Bienestar - Tus credenciales de acceso'
    
    mensaje = f"""
    ¡Hola {nombre_completo}!
    
    Tu caracterización ha sido registrada exitosamente. Ya tienes acceso a la plataforma SENA Bienestar.
    
    📱 TUS CREDENCIALES DE ACCESO:
    
    Usuario: {documento}
    Contraseña temporal: {password}
    
    🔐 IMPORTANTE:
    - Por seguridad, debes cambiar tu contraseña en el primer ingreso
    - No compartas estas credenciales con nadie
    - Si olvidaste tu contraseña, puedes recuperarla desde la app
    
    🌟 ¿QUÉ PUEDES HACER AHORA?
    
    ✅ Ver convocatorias de sostenimiento y beneficios
    ✅ Postularte a convocatorias disponibles
    ✅ Actualizar tu caracterización cada trimestre
    ✅ Consultar tus postulaciones y resultados
    
    📲 Ingresa a la plataforma para comenzar.
    
    ¡Gracias por ser parte de nuestra comunidad SENA!
    
    ---
    Este es un correo automático, por favor no responder.
    Si tienes problemas para acceder, contacta a tu coordinador de bienestar.
    """
    
    try:
        send_mail(
            asunto,
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False


# ============================================
# VISTAS PÚBLICAS (SIN LOGIN)
# ============================================

def landing_page(request):
    """Página de inicio que invita a llenar la caracterización"""
    context = {
        'tiene_usuario': request.user.is_authenticated
    }
    return render(request, 'caracterizacion/landing.html', context)


def iniciar_caracterizacion(request):
    """
    Vista para iniciar el proceso de caracterización pública.
    Verifica si el documento ya existe o tiene una caracterización en curso.
    """
    if request.method == 'POST':
        documento = request.POST.get('documento', '').strip()

        # Validar documento vacío
        if not documento:
            messages.error(request, 'Por favor ingresa tu número de documento')
            return redirect('iniciar_caracterizacion')

        # Verificar si ya existe un usuario con ese documento
        if Usuario.objects.filter(documento=documento).exists():
            messages.warning(
                request,
                'Ya existe una cuenta con este documento. Por favor inicia sesión.'
            )
            return redirect('login')

        # Verificar si ya tiene una caracterización en proceso
        caracterizacion_existente = Caracterizacion.objects.filter(
            documento_solicitante=documento,
            completada=False
        ).first()

        if caracterizacion_existente:
            # Continuar con la caracterización existente
            return redirect('formulario_caracterizacion', pk=caracterizacion_existente.id)

        # --- Crear nueva caracterización ---
        anio_actual = datetime.now().year
        mes_actual = datetime.now().month

        caracterizaciones_previas = Caracterizacion.objects.filter(
            documento_solicitante=documento
        ).order_by('anio', 'trimestre')

        # Determinar el trimestre
        if not caracterizaciones_previas.exists():
            trimestre = 'T1'
        else:
            ultima = caracterizaciones_previas.last()
            ultimo_trimestre = ultima.trimestre
            ultimo_anio = ultima.anio

            if ultimo_anio < anio_actual:
                trimestre = 'T1'
            else:
                if ultimo_trimestre == 'T1':
                    trimestre = 'T2'
                elif ultimo_trimestre == 'T2':
                    trimestre = 'T3'
                elif ultimo_trimestre == 'T3':
                    trimestre = 'T4'
                else:
                    trimestre = 'T1'  # Reinicia si ya llegó a T4

        # ✅ Crear la caracterización (siempre, sin depender de los if anteriores)
        caracterizacion = Caracterizacion.objects.create(
            documento_solicitante=documento,
            anio=anio_actual,
            trimestre=trimestre,
            ip_registro=obtener_cliente_ip(request)
        )

        # --- Crear preguntas desde la plantilla inicial ---
        plantilla = PlantillaCaracterizacion.objects.filter(
            es_plantilla_inicial=True,
            activa=True
        ).first()

        if plantilla:
            for pregunta_plantilla in plantilla.preguntas_plantilla.all():
                PreguntaCaracterizacion.objects.create(
                    id_caracterizacion=caracterizacion,
                    pregunta=pregunta_plantilla.pregunta,
                    tipo_pregunta=pregunta_plantilla.tipo_pregunta,
                    obligatoria=pregunta_plantilla.obligatoria,
                    opciones=pregunta_plantilla.opciones,
                    orden=pregunta_plantilla.orden
                )

        # Redirigir al formulario
        return redirect('formulario_caracterizacion', pk=caracterizacion.id)

    # Si no es POST, renderiza la vista normal
    return render(request, 'caracterizacion/iniciar.html')



# REEMPLAZAR la vista formulario_caracterizacion en views_aprendiz.py

def formulario_caracterizacion(request, pk=None):
    """
    Vista unificada para el formulario de caracterización
    Puede recibir un pk de caracterización existente o crear una nueva
    """
    caracterizacion_existente = None
    
    # Si viene un pk, cargar caracterización existente
    if pk:
        caracterizacion_existente = get_object_or_404(Caracterizacion, pk=pk)
        
        # Si ya fue completada, redirigir
        if caracterizacion_existente.completada:
            messages.info(request, 'Esta caracterización ya fue completada')
            return redirect('landing_page')
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # ============================================
                # 1. EXTRAER DATOS DEL FORMULARIO
                # ============================================
                
                # Datos Personales
                nombres = request.POST.get('nombres', '').strip()
                apellidos = request.POST.get('apellidos', '').strip()
                numero_identificacion = request.POST.get('numero_identificacion', '').strip()
                correo_electronico = request.POST.get('correo_electronico', '').strip()
                telefono = request.POST.get('telefono', '').strip()
                fecha_nacimiento = request.POST.get('fecha_nacimiento', '')
                genero = request.POST.get('genero', '')
                genero_otro = request.POST.get('genero_otro', '')
                estado_civil = request.POST.get('estado_civil', '')
                nivel_educativo = request.POST.get('nivel_educativo', '')
                grupo_etnico = request.POST.get('grupo_etnico', '')
                grupo_etnico_otro = request.POST.get('grupo_etnico_otro', '')
                estrato = request.POST.get('estrato', '')
                barrio_residencia = request.POST.get('barrio_residencia', '')
                comuna = request.POST.get('comuna', '')
                ocupacion = request.POST.get('ocupacion', '')
                ocupacion_otro = request.POST.get('ocupacion_otro', '')
                tiene_hijos = request.POST.get('tiene_hijos', '')
                cuantos_hijos = request.POST.get('cuantos_hijos', '')
                
                # Contexto Familiar y Social
                vive_con = request.POST.get('vive_con', '')
                cabeza_hogar = request.POST.get('cabeza_hogar', '')
                cabeza_hogar_otro = request.POST.get('cabeza_hogar_otro', '')
                tipo_vivienda = request.POST.get('tipo_vivienda', '')
                num_personas = request.POST.get('num_personas', '')
                acceso_internet = request.POST.get('acceso_internet', '')
                equipo_propio = request.POST.get('equipo_propio', '')
                responsable_hogar = request.POST.get('responsable_hogar', '')
                formacion_prioridad = request.POST.get('formacion_prioridad', '')
                apoyo_emocional = request.POST.get('apoyo_emocional', '')
                
                # Ubicación y Transporte
                distancia = request.POST.get('distancia', '')
                transporte = request.POST.get('transporte', '')
                tiempo_desplazamiento = request.POST.get('tiempo_desplazamiento', '')
                costo_transporte = request.POST.get('costo_transporte', '')
                inconvenientes_transporte = request.POST.get('inconvenientes_transporte', '')
                
                # Aspectos Académicos
                programa_inscrito = request.POST.get('programa_inscrito', '')
                por_que_programa = request.POST.get('por_que_programa', '')
                apoyos_importantes = request.POST.get('apoyos_importantes', '')
                pensado_dejar = request.POST.get('pensado_dejar', '')
                motivos_dificultad = request.POST.getlist('motivos_dificultad')
                apoyos_externos = request.POST.get('apoyos_externos', '')
                apoyos_suficientes = request.POST.get('apoyos_suficientes', '')
                jornada = request.POST.get('jornada', '')
                dificultades_formacion = request.POST.getlist('dificultades_formacion')
                etapa_dificultades = request.POST.get('etapa_dificultades', '')
                apoyo_necesita = request.POST.getlist('apoyo_necesita')
                horas_estudio = request.POST.get('horas_estudio', '')
                probabilidad_finalizar = request.POST.get('probabilidad_finalizar', '')
                
                # Salud y Bienestar
                afiliacion_eps = request.POST.get('afiliacion_eps', '')
                condicion_salud = request.POST.get('condicion_salud', '')
                condicion_salud_desc = request.POST.get('condicion_salud_desc', '')
                condicion_psicologica = request.POST.get('condicion_psicologica', '')
                apoyo_psicologico = request.POST.get('apoyo_psicologico', '')
                fortalecer_salud_mental = request.POST.get('fortalecer_salud_mental', '')
                cambios_emocionales = request.POST.get('cambios_emocionales', '')
                actividad_fisica = request.POST.get('actividad_fisica', '')
                ansiedad_estres = request.POST.get('ansiedad_estres', '')
                emociones_desempeno = request.POST.get('emociones_desempeno', '')
                dificultad_concentracion = request.POST.get('dificultad_concentracion', '')
                
                # Aspectos Tecnológicos
                dispositivos_tecnologicos = request.POST.get('dispositivos_tecnologicos', '')
                dificultades_internet = request.POST.get('dificultades_internet', '')
                comparte_dispositivo = request.POST.get('comparte_dispositivo', '')
                
                # Aspectos Psicológicos y Emocionales
                presion_continuar = request.POST.get('presion_continuar', '')
                decision_ingreso = request.POST.get('decision_ingreso', '')
                ejercer_conocimientos = request.POST.get('ejercer_conocimientos', '')
                apoyo_mejoraria = request.POST.get('apoyo_mejoraria', '')
                valoran_esfuerzo = request.POST.get('valoran_esfuerzo', '')
                influencia_positiva = request.POST.get('influencia_positiva', '')
                discriminacion = request.POST.get('discriminacion', '')
                discriminacion_desc = request.POST.get('discriminacion_desc', '')
                cambio_residencia = request.POST.get('cambio_residencia', '')
                perdida_conflicto = request.POST.get('perdida_conflicto', '')
                afectacion_conflicto = request.POST.get('afectacion_conflicto', '')
                dificultad_pedir_ayuda = request.POST.get('dificultad_pedir_ayuda', '')
                conflicto_dinamica_familiar = request.POST.get('conflicto_dinamica_familiar', '')
                perdida_bienestar = request.POST.get('perdida_bienestar', '')
                
                # Términos y Condiciones
                acepta_terminos = request.POST.get('acepta_terminos') == 'on'
                
                # ============================================
                # 2. VALIDACIONES BÁSICAS
                # ============================================
                
                if not acepta_terminos:
                    messages.error(request, 'Debes aceptar los términos y condiciones')
                    return redirect('formulario_caracterizacion', pk=pk) if pk else redirect('iniciar_caracterizacion')
                
                if not all([nombres, apellidos, numero_identificacion, correo_electronico]):
                    messages.error(request, 'Por favor completa todos los campos obligatorios')
                    return redirect('formulario_caracterizacion', pk=pk) if pk else redirect('iniciar_caracterizacion')
                
                # Verificar si ya existe usuario con ese documento
                if Usuario.objects.filter(documento=numero_identificacion).exists():
                    messages.warning(request, 'Ya existe una cuenta con este documento. Por favor inicia sesión.')
                    return redirect('admin:login')
                
                if Usuario.objects.filter(email=correo_electronico).exists():
                    messages.warning(request, 'Ya existe una cuenta con este correo electrónico.')
                    return redirect('admin:login')
                
                # ============================================
                # 3. CREAR O ACTUALIZAR CARACTERIZACIÓN
                # ============================================
                
                if caracterizacion_existente:
                    # Actualizar existente
                    caracterizacion = caracterizacion_existente
                    caracterizacion.email_solicitante = correo_electronico
                    caracterizacion.telefono_solicitante = telefono
                    caracterizacion.acepta_terminos = True
                    caracterizacion.fecha_aceptacion_terminos = timezone.now()
                    caracterizacion.completada = True
                    caracterizacion.usuario_creado_desde_caracterizacion = True
                    caracterizacion.save()
                    
                    # Eliminar respuestas anteriores
                    caracterizacion.respuestas.all().delete()
                    caracterizacion.preguntas.all().delete()
                else:
                    # Crear nueva
                    anio_actual = datetime.now().year
                    mes_actual = datetime.now().month
                    
                    # Calcular trimestre según el mes
                    if mes_actual <= 3:
                        trimestre = 'T1'
                    elif mes_actual <= 6:
                        trimestre = 'T2'
                    elif mes_actual <= 9:
                        trimestre = 'T3'
                    else:
                        trimestre = 'T4'
                    
                    caracterizacion = Caracterizacion.objects.create(
                        documento_solicitante=numero_identificacion,
                        email_solicitante=correo_electronico,
                        telefono_solicitante=telefono,
                        anio=anio_actual,
                        trimestre=trimestre,
                        acepta_terminos=True,
                        fecha_aceptacion_terminos=timezone.now(),
                        ip_registro=obtener_cliente_ip(request),
                        completada=True,
                        usuario_creado_desde_caracterizacion=True
                    )
                
                # ============================================
                # 4. CREAR PREGUNTAS Y RESPUESTAS
                # ============================================
                
                # Diccionario con todas las respuestas organizadas
                respuestas_data = {
                    # Datos Personales
                    'Nombres': nombres,
                    'Apellidos': apellidos,
                    'Número de Identificación': numero_identificacion,
                    'Correo Electrónico': correo_electronico,
                    'Teléfono': telefono,
                    'Fecha de Nacimiento': fecha_nacimiento,
                    'Género': f"{genero} - {genero_otro}" if genero == 'Otro' else genero,
                    'Estado Civil': estado_civil,
                    'Nivel Educativo': nivel_educativo,
                    'Grupo Étnico': f"{grupo_etnico} - {grupo_etnico_otro}" if grupo_etnico == 'Otro' else grupo_etnico,
                    'Estrato Socioeconómico': estrato,
                    'Barrio de Residencia': barrio_residencia,
                    'Comuna': comuna,
                    'Ocupación Actual': f"{ocupacion} - {ocupacion_otro}" if ocupacion == 'Otro' else ocupacion,
                    '¿Tiene hijos?': tiene_hijos,
                    'Cuántos hijos': cuantos_hijos if tiene_hijos == 'Si' else 'N/A',
                    
                    # Contexto Familiar y Social
                    '¿Con quién vive actualmente?': vive_con,
                    '¿Quién es la cabeza del hogar?': f"{cabeza_hogar} - {cabeza_hogar_otro}" if cabeza_hogar == 'Otro' else cabeza_hogar,
                    'Tipo de vivienda': tipo_vivienda,
                    'Número de personas que viven con usted': num_personas,
                    '¿Tiene acceso a internet en su hogar?': acceso_internet,
                    '¿Cuenta con equipo propio para estudiar?': equipo_propio,
                    '¿Es usted responsable del hogar?': responsable_hogar,
                    '¿Su familia considera su formación una prioridad?': formacion_prioridad,
                    '¿Cuenta con apoyo emocional?': apoyo_emocional,
                    
                    # Ubicación y Transporte
                    'Distancia al centro de formación': distancia,
                    'Medio de transporte principal': transporte,
                    'Tiempo de desplazamiento': tiempo_desplazamiento,
                    '¿El costo del transporte le dificulta continuar?': costo_transporte,
                    '¿Tiene inconvenientes con el transporte?': inconvenientes_transporte,
                    
                    # Aspectos Académicos
                    'Programa inscrito': programa_inscrito,
                    '¿Por qué eligió este programa?': por_que_programa,
                    'Apoyos importantes para continuar': apoyos_importantes,
                    '¿Ha pensado en dejar el programa?': pensado_dejar,
                    'Motivos que dificultan la continuidad': ', '.join(motivos_dificultad) if motivos_dificultad else 'Ninguno',
                    '¿Ha solicitado apoyos externos?': apoyos_externos,
                    '¿Los apoyos han sido suficientes?': apoyos_suficientes if apoyos_externos == 'Si' else 'N/A',
                    'Jornada': jornada,
                    'Dificultades en la formación': ', '.join(dificultades_formacion) if dificultades_formacion else 'Ninguna',
                    'Etapa con más dificultades': etapa_dificultades,
                    'Apoyo que necesita': ', '.join(apoyo_necesita) if apoyo_necesita else 'Ninguno',
                    'Horas de estudio fuera de jornada': horas_estudio,
                    'Probabilidad de finalizar': probabilidad_finalizar,
                    
                    # Salud y Bienestar
                    '¿Cuenta con afiliación a EPS?': afiliacion_eps,
                    '¿Tiene condición de salud o discapacidad?': f"{condicion_salud} - {condicion_salud_desc}" if condicion_salud == 'Si' else condicion_salud,
                    '¿Diagnóstico psicológico profesional?': condicion_psicologica,
                    '¿Ha recibido apoyo psicológico?': apoyo_psicologico,
                    '¿SENA debería fortalecer salud mental?': fortalecer_salud_mental,
                    '¿Cambios emocionales que afecten desempeño?': cambios_emocionales,
                    'Frecuencia de actividad física': actividad_fisica,
                    'Frecuencia de ansiedad o estrés': ansiedad_estres,
                    'Influencia de emociones en desempeño': emociones_desempeno,
                    'Dificultad para concentrarse': dificultad_concentracion,
                    
                    # Aspectos Tecnológicos
                    '¿Cuenta con dispositivos tecnológicos?': dispositivos_tecnologicos,
                    '¿Dificultades de conexión a internet?': dificultades_internet,
                    '¿Comparte dispositivo de estudio?': comparte_dispositivo,
                    
                    # Aspectos Psicológicos y Emocionales
                    '¿Siente presión para continuar?': presion_continuar,
                    'Decisión de ingreso al programa': decision_ingreso,
                    '¿Piensa ejercer los conocimientos?': ejercer_conocimientos,
                    '¿Apoyo emocional mejoraría experiencia?': apoyo_mejoraria,
                    '¿Valoran su esfuerzo?': valoran_esfuerzo,
                    '¿Influencia positiva en aprendizaje?': influencia_positiva,
                    '¿Ha sido víctima de discriminación?': f"{discriminacion} - {discriminacion_desc}" if discriminacion == 'Si' else discriminacion,
                    '¿Cambio de residencia por conflicto?': cambio_residencia,
                    '¿Pérdida familiar por conflicto?': perdida_conflicto,
                    'Afectación del conflicto en vida diaria': afectacion_conflicto,
                    'Dificultad para pedir ayuda': dificultad_pedir_ayuda,
                    'Influencia del conflicto en dinámica familiar': conflicto_dinamica_familiar,
                    'Afectación de pérdida en bienestar emocional': perdida_bienestar,
                }
                
                # Crear preguntas y respuestas
                orden = 1
                for pregunta_texto, respuesta_texto in respuestas_data.items():
                    pregunta = PreguntaCaracterizacion.objects.create(
                        id_caracterizacion=caracterizacion,
                        pregunta=pregunta_texto,
                        tipo_pregunta='texto',
                        obligatoria=True,
                        orden=orden
                    )
                    
                    RespuestaCaracterizacion.objects.create(
                        id_caracterizacion=caracterizacion,
                        id_pregunta=pregunta,
                        respuesta=str(respuesta_texto) if respuesta_texto else ''
                    )
                    
                    orden += 1
                
                # ============================================
                # 5. CREAR USUARIO Y APRENDIZ
                # ============================================
                
                resultado = crear_usuario_desde_caracterizacion(
                    caracterizacion=caracterizacion,
                    nombres=nombres,
                    apellidos=apellidos,
                    email=correo_electronico,
                    telefono=telefono
                )
                
                if resultado['exito']:
                    messages.success(
                        request,
                        f'¡Registro exitoso! Revisa tu correo {correo_electronico} para obtener tus credenciales de acceso.'
                    )
                    return redirect('registro_completado')
                else:
                    messages.error(request, f'Error al crear usuario: {resultado["error"]}')
                    return redirect('iniciar_caracterizacion')
        
        except Exception as e:
            messages.error(request, f'Error al procesar el formulario: {str(e)}')
            return redirect('iniciar_caracterizacion')
    
    # GET: Mostrar formulario
    context = {
        'caracterizacion': caracterizacion_existente,
        'progreso': caracterizacion_existente.obtener_progreso() if caracterizacion_existente else 0
    }
    
    return render(request, 'caracterizacion/formulario_completado.html', context)
    

def registro_completado(request):
    return render(request, 'caracterizacion/registro_completado.html')


@transaction.atomic
def crear_usuario_desde_caracterizacion(caracterizacion, nombres, apellidos, email, telefono=None):
    """
    Crea usuario y aprendiz a partir de una caracterización completada
    """
    try:
        documento = caracterizacion.documento_solicitante
        
        # Verificar que no exista el usuario
        if Usuario.objects.filter(documento=documento).exists():
            return {'exito': False, 'error': 'Ya existe un usuario con este documento'}
        
        if Usuario.objects.filter(email=email).exists():
            return {'exito': False, 'error': 'Ya existe un usuario con este correo electrónico'}
        
        # Generar contraseña temporal
        password_temporal = generar_password_temporal()
        
        # Crear usuario
        usuario = Usuario.objects.create_user(
            username=documento,
            email=email,
            password=password_temporal,
            first_name=nombres or '',
            last_name=apellidos or '',
            documento=documento,
            rol='aprendiz',
            estado=True,
            primer_ingreso=True,
            debe_cambiar_password=True
        )
        
        # Crear perfil de aprendiz
        aprendiz = Aprendiz.objects.create(
            apUsuario=usuario,
            documento_temp=documento,
            nombres_temp=nombres,
            apellidos_temp=apellidos,
            email_temp=email,
            telefono_temp=telefono,
            usuario_creado=True,
            estado=True
        )
        
        # Vincular caracterización al aprendiz
        caracterizacion.id_aprendiz = aprendiz
        caracterizacion.usuario_creado_desde_caracterizacion = True
        caracterizacion.save()
        
        # Enviar credenciales por correo
        nombre_completo = f"{nombres} {apellidos}"
        envio_exitoso = enviar_credenciales_correo(
            email,
            documento,
            password_temporal,
            nombre_completo
        )
        
        return {
            'exito': True,
            'usuario': usuario,
            'aprendiz': aprendiz,
            'password': password_temporal,
            'envio_correo': envio_exitoso,
            'error': None
        }
        
    except Exception as e:
        return {'exito': False, 'error': str(e)}

# ============================================
# VISTAS CON LOGIN
# ============================================


@login_required
def panel_coordinador_instructores(request):
    return render(request, 'panel_coordinador_instructores.html')

def login_view(request):
    """
    Vista de login personalizada con mensaje para aprendices
    """
    if request.user.is_authenticated:
        # Si ya está autenticado, redirigir al dashboard
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
        
                # Verificar si debe cambiar contraseña (solo aprendices)
                if user.rol == 'aprendiz' and user.debe_cambiar_password:
                    return redirect('cambiar_password_inicial')
                
                # Redirigir según el rol
                return redirigir_segun_rol(user)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
def redirigir_segun_rol(user):
    """
    Función auxiliar para redirigir al usuario según su rol
    """
    if user.rol == 'coordinadorInstructores':
        return redirect('panel_coordinador_instructores')
    
    elif user.rol == 'coordinadorBienestar':
        return redirect('panel_coordinador_bienestar')
    
    elif user.rol == 'instructor':
        return redirect('panel_instructor')
    
    elif user.rol == 'funcionario':
        return redirect('panel_funcionario')
    

    
    else:
        messages.error(None, 'Rol de usuario no reconocido.')
        return redirect('login')


def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('landing_page')
@login_required
def cambiar_password_inicial(request):
    """
    Vista para cambiar la contraseña en el primer ingreso (solo aprendices)
    """
    # Solo los aprendices deben cambiar contraseña

    if not request.user.debe_cambiar_password:
        return redirect('dashboard')
    
    if request.method == 'POST':
        nueva_password = request.POST.get('nueva_password')
        confirmar_password = request.POST.get('confirmar_password')
        
        if nueva_password != confirmar_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('cambiar_password_inicial')
        
        if len(nueva_password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return redirect('cambiar_password_inicial')
        
        # Cambiar contraseña
        request.user.set_password(nueva_password)
        request.user.debe_cambiar_password = False
        request.user.primer_ingreso = False
        request.user.save()
        
        # Re-autenticar
        user = authenticate(username=request.user.username, password=nueva_password)
        login(request, user)
        
        messages.success(request, '¡Contraseña actualizada exitosamente!')
        return redirect('dashboard')
    
    return render(request, 'caracterizacion/cambiar_password.html')

@login_required
def dashboard(request):
    """Dashboard principal según el rol del usuario"""
    # Si debe cambiar password, redirigir
    if request.user.debe_cambiar_password:
        return redirect('cambiar_password_inicial')
    
    usuario = request.user
    
    if usuario.rol == 'aprendiz':
        try:
            aprendiz = usuario.aprendiz
            
            # Importar aquí para evitar importación circular
            from .models import Convocatoria, Postulacion
            
            context = {
                'aprendiz': aprendiz,
                'convocatorias_abiertas': Convocatoria.objects.filter(
                    con_fecha_inicio__lte=timezone.now(),
                    con_fecha_final__gte=timezone.now()
                ).count(),
                'mis_postulaciones': Postulacion.objects.filter(
                    pos_aprendiz=aprendiz
                ).count(),
                'caracterizacion_actual': aprendiz.caracterizaciones.filter(
                    anio=datetime.now().year
                ).first()
            }
            
            return render(request, 'dashboard/aprendiz.html', context)
            
        except Aprendiz.DoesNotExist:
            messages.error(request, 'No tienes un perfil de aprendiz asociado')
            return redirect('landing_page')
    
    # Otros roles...
    return render(request, 'dashboard/general.html', {'usuario': usuario})
# ============================================
# VISTAS CON LOGIN - COORDINADORES Y OTROS ROLES
# ============================================

@login_required
def panel_coordinador_instructores(request):
    """Panel para coordinador de instructores"""
    if not request.user.tiene_rol('coordinadorInstructores'):
             return JsonResponse({"error": "No tienes permisos para acceder a esta sección"}, status=403)
    
    return render(request, 'panel_coordinador_instructores.html')


@login_required
def panel_coordinador_bienestar(request):
    """Panel para coordinador de bienestar"""
    if not request.user.tiene_rol('coordinadorBienestar'):
        return JsonResponse({"error": "No tienes permisos para acceder a esta sección"}, status=403)
        return redirect('dashboard')
    
    return render(request, 'panel_coordinador_bienestar.html')


@login_required
def panel_instructor(request):
    """Panel para instructores"""
   # if not request.user.tiene_rol('instructor'):
    #    messages.error(request, 'No tienes permisos para acceder a esta sección')
     #   return redirect('dashboard')
    
    return render(request, 'panel_instructor.html')


@login_required
def panel_funcionario(request):
    """Panel para funcionarios"""
    if not request.user.tiene_rol('funcionario'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    return render(request, 'panel_funcionario.html')


@login_required
def dashboard(request):
    """Dashboard general - redirige según el rol"""
    return redirigir_segun_rol(request.user)