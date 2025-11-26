from django.db import models

class Municipio(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]
    
    nombre = models.CharField(
        max_length=150, 
        unique=True,
        verbose_name="Nombre del Municipio / Corregimiento",
        help_text="Ingrese el nombre del municipio o corregimiento."
    )

    status = models.CharField(
        max_length=8, 
        choices=STATUS_CHOICES, 
        default='ACTIVE',
        verbose_name='Estado',
        help_text="Estado actual (Activo/Inactivo)."
    )

    class Meta:
        verbose_name = "Municipio / Corregimiento"
        verbose_name_plural = "Municipios / Corregimientos"

    def __str__(self):
        return self.nombre
