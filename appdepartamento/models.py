from django.db import models

class Departamento(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]

    nombre = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Nombre", 
        help_text="Ingrese el nombre del departamento."
        )

    status = models.CharField(
        max_length=8, 
        choices=STATUS_CHOICES, 
        default='ACTIVE',
        verbose_name='Estado',
        help_text="Estado actual (Activo/Inactivo)."
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "departamento"
        verbose_name_plural = "departamentos"