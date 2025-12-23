from django.db import models
from django.core.exceptions import ValidationError

from smart_selects.db_fields import ChainedForeignKey

from AppMunicipio.models import Municipio
from appcorregimientos.models import Corregimiento
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

    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.PROTECT,
        verbose_name="Departamento"
    )
    
    municipio = ChainedForeignKey(
        Municipio,
        chained_field="departamento",
        chained_model_field="departamento",
        show_all=False, 
        on_delete=models.PROTECT,
        verbose_name="Municipio",
        help_text="Seleccione la ubicación geográfica del puesto."
    )

    corregimiento = ChainedForeignKey(
        Corregimiento,
        chained_field="municipio",
        chained_model_field="municipio",
        show_all=False,
        auto_choose=False,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Corregimiento"
    )

    status = models.CharField(
        max_length=8, 
        choices=STATUS_CHOICES, 
        default='ACTIVE',
        verbose_name='Estado',
        help_text="Estado actual (Activo/Inactivo)."
    )

    def clean(self):
        if self.corregimiento and self.corregimiento.municipio != self.municipio:
            raise ValidationError(
                "El corregimiento no pertenece al municipio seleccionado."
            )

    def __str__(self):
        return f"{self.nombre_lugar} – {self.municipio}"

    class Meta:
        verbose_name = "Puesto de Votación"
        verbose_name_plural = "Puestos de Votación"
