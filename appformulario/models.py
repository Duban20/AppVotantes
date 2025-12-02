from django.db import models

from AppMunicipio.models import Municipio
from AppPuestoVotacion.models import PuestoVotacion
from applider.models import Lider
from appmesa.models import Mesa

class votante(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]

    nombre = models.CharField(
        max_length=100, 
        verbose_name="Nombres", 
        help_text="Ingrese los nombres del votante."
    )
    
    apellido = models.CharField(
        max_length=100, 
        verbose_name="Apellidos", 
        help_text="Ingrese los apellidos del votante."
    )
    
    cedula = models.CharField(
        max_length=12, 
        verbose_name="Cédula", 
        help_text="Ingrese la cédula sin guiones ni espacios.", 
        unique=True
    )
    
    direccion_residencia = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name="Dirección de residencia",
        help_text="Ingrese la dirección de residencia del votante."
    )    

    telefono = models.CharField(
        max_length=100, 
        verbose_name="Teléfono",
        help_text="Ingrese un número de contacto."
    )
    
    lider = models.ForeignKey(
        Lider,
        on_delete=models.PROTECT,
        verbose_name="Líder",
        help_text="Seleccione el líder responsable del votante."
    )

    mesa = models.ForeignKey(
        Mesa,
        on_delete=models.PROTECT,                
        verbose_name="Mesa de Votación",
        help_text="Seleccione."
    )

    municipio_nacimiento = models.ForeignKey(
        Municipio,
        on_delete=models.PROTECT,
        verbose_name="Lugar de nacimiento.",
        help_text="Seleccione el lugar de nacimiento."
    ) 

    status = models.CharField(
        max_length=8, 
        choices=STATUS_CHOICES, 
        default='ACTIVE',
        verbose_name='Estado',
        help_text="Estado actual (Activo/Inactivo)."
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.mesa.numero}"

    class Meta:
        verbose_name = "votante"
        verbose_name_plural = "votantes"