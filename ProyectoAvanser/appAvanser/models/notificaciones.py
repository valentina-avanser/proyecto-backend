from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings

    
#HU010 y HU016 Notificaciones
class Notificacion(models.Model):
    TIPOS = [
        ("alerta", "Alerta"),
        ("recordatorio", "Recordatorio"),
        ("mensaje", "Mensaje"),
        ("info", "Información"),
        ("emergencia", "Emergencia"),
    ]
    PRIORIDADES = [
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta"),
    ]

    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE, related_name="notificaciones")
    tipo = models.CharField(max_length=20, choices=TIPOS, default="mensaje")
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default="media")
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    enviar_correo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} → {self.usuario.nombre}"

    class Meta:
        ordering = ["-fecha_creacion"]
        

    # 🔔 Mtodo para envío automático de correo
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.enviar_correo or self.prioridad == "alta" or self.tipo == "emergencia":
            self.enviar_notificacion_email()

    def enviar_notificacion_email(self):
        """Envía una notificación por correo al instructor."""
        try:
            if self.usuario.email:
                asunto = f"[AVANSER] {self.titulo}"
                mensaje = f"{self.contenido}\n\nPrioridad: {self.get_prioridad_display()}"
                correo = EmailMessage(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [self.usuario.email])
                correo.send(fail_silently=True)
        except Exception as e:
            print(f"Error enviando correo: {e}")