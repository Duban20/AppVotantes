from django.db import models
from appdepartamento.models import Departamento
from AppMunicipio.models import Municipio

class Corregimiento(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]
    
    nombre = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre del Corregimiento",
        help_text="Ingrese el nombre del corregimiento."
    )

    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.PROTECT,
        related_name='corregimientos',
        verbose_name="Municipio",
        help_text="Seleccione el municipio al que pertenece."
    )

    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        verbose_name='Estado',
        help_text="Estado actual (Activo/Inactivo)."
    )

    class Meta:
        verbose_name = "Corregimiento"
        verbose_name_plural = "Corregimientos"

    def __str__(self):
        return self.nombre
