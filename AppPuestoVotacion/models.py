from django.db import models
from django.core.exceptions import ValidationError

from AppMunicipio.models import Municipio
from appdepartamento.models import Departamento

class PuestoVotacion(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]

    nombre_lugar = models.CharField(
        max_length=200, 
        unique=True, 
        verbose_name="Nombre del puesto", 
        help_text="Ingrese el nombre del puesto de votación.")
    
    direccion = models.CharField(
        max_length=100,
        verbose_name="Dirección",
        blank=True, null=True,
        help_text="Ingrese la dirección del puesto (opcional)"
    )
    
    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.PROTECT,
        verbose_name="Municipio o Corregimiento",
        help_text="Seleccione la ubicación geográfica del puesto."
    )

    status = models.CharField(
        max_length=8, 
        choices=STATUS_CHOICES, 
        default='ACTIVE',
        verbose_name='Estado',
        help_text="Estado actual (Activo/Inactivo)."
    )

    def __str__(self):
        return f"{self.nombre_lugar} – {self.municipio}"

    class Meta:
        verbose_name = "Puesto de Votación"
        verbose_name_plural = "Puestos de Votación"
