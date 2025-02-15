from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    prioridad = models.CharField(
        max_length=50, 
        choices=[
            ('Alta', 'Alta'), 
            ('Media', 'Media'), 
            ('Baja', 'Baja')
        ]
    )

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
