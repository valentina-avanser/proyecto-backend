from rest_framework import permissions

class IsApplicationAdmin(permissions.BasePermission):
    """
    Permite acceso solo a usuarios cuyo campo 'rol' es 'Administrador'.
    Asegúrate de que 'rol' sea el nombre del campo en tu modelo de usuario.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.rol == 'Administrador'
    
class IsInstructor(permissions.BasePermission):
    """Permite acceso solo a usuarios cuyo campo 'rol' es 'Instructor'."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.rol == 'Instructor'