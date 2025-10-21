import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.db import transaction
from appAvanser.models import Usuario, Instructor
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken  



@login_required  # ✅ Asegura que el usuario esté autenticado
@require_http_methods(["POST"])  # ✅ Solo permite POST
def cargar_instructores(request):
    """
    Vista para cargar instructores desde un archivo JSON
    Solo accesible para coordinadores de instructores autenticados
    """
    
    # ✅ Verificar rol de coordinador de instructores
    if not request.user.is_authenticated or not request.user.tiene_rol('coordinadorInstructores'):
        return JsonResponse({"error": "No tienes permisos para acceder a esta sección"}, status=403)


    # ✅ Verificar que se envió un archivo
    archivo = request.FILES.get("archivo")
    if not archivo:
        return JsonResponse({
            "error": "No se ha enviado ningún archivo"
        }, status=400)

    # ✅ Validar que el archivo sea JSON
    if not archivo.name.endswith('.json'):
        return JsonResponse({
            "error": "El archivo debe tener extensión .json"
        }, status=400)

    # ✅ Leer y parsear el archivo JSON
    try:
        contenido = archivo.read().decode('utf-8')
        data = json.loads(contenido)
    except json.JSONDecodeError as e:
        return JsonResponse({
            "error": f"El archivo no tiene un formato JSON válido: {str(e)}"
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "error": f"Error al leer el archivo: {str(e)}"
        }, status=400)

    # ✅ Validar que sea una lista
    if not isinstance(data, list):
        return JsonResponse({
            "error": "El JSON debe contener una lista de instructores"
        }, status=400)

    nuevos = 0
    existentes = 0
    errores = []

    # ✅ Procesar instructores dentro de una transacción
    try:
        with transaction.atomic():
            for index, item in enumerate(data, start=1):
                try:
                    # Validar campos obligatorios
                    documento = item.get("documento", "").strip()
                    email = item.get("email", "").strip()
                    username = item.get("username", "").strip()
                    first_name = item.get("first_name", "").strip()
                    last_name = item.get("last_name", "").strip()

                    if not all([documento, email, username, first_name, last_name]):
                        errores.append({
                            "linea": index,
                            "error": "Faltan datos obligatorios (documento, email, username, first_name, last_name)",
                            "data": item
                        })
                        continue

                    # ✅ Crear o actualizar usuario
                    usuario, usuario_creado = Usuario.objects.get_or_create(
                        documento=documento,
                        defaults={
                            "username": username,
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "rol": "instructor",
                            "password": make_password(documento),  # Contraseña = documento
                            "debe_cambiar_password": True,  # Debe cambiar en primer ingreso
                        }
                    )

                    # Si el usuario ya existía, actualizar email si es diferente
                    if not usuario_creado:
                        if usuario.email != email:
                            usuario.email = email
                            usuario.save()

                    # ✅ Crear instructor si no existe
                    instructor, instructor_creado = Instructor.objects.get_or_create(
                        instUsuario=usuario,
                        defaults={
                            "especialidad": item.get("especialidad", "No especificada"),
                            "competencia": item.get("competencia", ""),
                        }
                    )

                    # Actualizar especialidad y competencia si ya existía
                    if not instructor_creado:
                        instructor.especialidad = item.get("especialidad", instructor.especialidad)
                        instructor.competencia = item.get("competencia", instructor.competencia)
                        instructor.save()

                    if usuario_creado:
                        nuevos += 1
                    else:
                        existentes += 1

                except Exception as e:
                    errores.append({
                        "linea": index,
                        "error": str(e),
                        "data": item
                    })

    except Exception as e:
        return JsonResponse({
            "error": f"Error al procesar la transacción: {str(e)}"
        }, status=500)

    # ✅ Retornar respuesta con resumen
    return JsonResponse({
        "mensaje": "Carga completada exitosamente" if not errores else "Carga completada con errores",
        "nuevos_registros": nuevos,
        "registros_existentes": existentes,
        "total_procesados": nuevos + existentes,
        "errores": errores,
        "tiene_errores": len(errores) > 0
    })


@login_required
def interfaz_carga_instructores(request):
    """
    Interfaz para cargar instructores
    Solo accesible para coordinadores de instructores
    """
    if not request.user.tiene_rol("coordinadorInstructores"):
        return render(request, "error_403.html", {
            "mensaje": "No tienes permisos para acceder a esta sección"
        }, status=403)
    
    return render(request, "cargar_instructores.html")

    permission_classes = [IsAuthenticated]
