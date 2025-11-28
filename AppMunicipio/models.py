from django.db import models
from appdepartamento.models import Departamento

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

    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.PROTECT, 
        verbose_name="Departamento",
        help_text="Seleccione."
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
        return f"{self.nombre} – {self.departamento}"
