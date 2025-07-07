from django.db import models
from django.contrib.auth.models import User # Importamos el modelo de usuario de Django

# Create your models here.

class Consulta(models.Model):
    # Opciones para el tipo de consulta
    TIPO_CONSULTA_CHOICES = [
        ('basica', 'Consulta escrita básica (5.000 AR$ a 10.000 AR$)'),
        ('analisis', 'Consulta con análisis de campaña (15.000 AR$ a 25.000 AR$)'),
        ('llamada', 'Llamada de 30 minutos (30.000 AR$)'),
    ]

    # Opciones para el estado de la consulta
    ESTADO_CONSULTA_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultas')
    tipo = models.CharField(max_length=50, choices=TIPO_CONSULTA_CHOICES)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2) # Precio final de la consulta
    estado = models.CharField(max_length=50, choices=ESTADO_CONSULTA_CHOICES, default='pendiente')
    respuesta = models.TextField(blank=True, null=True) # La respuesta del analista, puede estar vacía
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Consulta de {self.user.username} - {self.get_tipo_display()} ({self.estado})"

class Pago(models.Model):
    # Opciones para el estado del pago
    ESTADO_PAGO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
    ]

    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, related_name='pago')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=50, choices=ESTADO_PAGO_CHOICES, default='pendiente')
    transaccion_id = models.CharField(max_length=255, blank=True, null=True, unique=True) # ID de transacción de la pasarela de pago

    def __str__(self):
        return f"Pago por consulta {self.consulta.id} - {self.monto} ({self.estado_pago})"
