from django.db import models
from django.core.exceptions import ValidationError

from AppMunicipio.models import Municipio

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
    
    aplica_direccion = models.BooleanField(
        default=True, 
        verbose_name="¿El puesto tiene dirección física?",
        )
    
    direccion = models.CharField(
        max_length=255,
        verbose_name="Dirección",
        blank=True,
        help_text="Ingrese la dirección del puesto o marque N/A si no aplica."
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
    
    def clean(self):
        """Se ejecuta antes de guardar desde formularios o admin."""
        if not self.aplica_direccion:
            # Si no aplica, forzamos valor "N/A"
            self.direccion = "N/A"
        else:
            # Si aplica, la dirección NO puede estar vacía
            if not self.direccion or self.direccion.strip() == "":
                raise ValidationError({"direccion": "Debe ingresar una dirección o marcar la casilla (N/A)."})

    def save(self, *args, **kwargs):
        # Garantiza que incluso al guardar desde código se respete la regla
        if not self.aplica_direccion:
            self.direccion = "N/A"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_lugar} – {self.direccion} – {self.municipio}"

    class Meta:
        verbose_name = "Puesto de Votación"
        verbose_name_plural = "Puestos de Votación"
