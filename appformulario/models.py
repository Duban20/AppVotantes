from django.db import models

from AppMunicipio.models import Municipio
from AppPuestoVotacion.models import PuestoVotacion
from appmesa.models import Mesa

class votante(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]

    ROLES = [
        ('LIDER_VOTANTE', 'Líder'),
        ('VOTANTE', 'Votante'),
    ]

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='VOTANTE',
        verbose_name="Rol"
    )

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

    municipio_residencia = models.ForeignKey(
        Municipio,
        on_delete=models.PROTECT,
        verbose_name="Municipio de Nacimiento",
        help_text="Seleccione el municipio de nacimiento",
    )
    
    direccion_residencia = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name="Dirección de residencia",
        help_text="Ingrese la dirección de residencia del votante."
    )    

    barrio_residencia = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name="Barrio",
        help_text="Barrio de residencia."
    )    

    telefono = models.CharField(
        max_length=100, 
        blank=True, null=True,
        verbose_name="Teléfono",
        help_text="Ingrese un número de contacto."
    )

    puesto_votacion = models.ForeignKey(
        PuestoVotacion,
        on_delete=models.PROTECT,
        verbose_name="Puesto de Votación",
        help_text="Seleccione el puesto de votación."
    )

    mesa = models.ForeignKey(
        Mesa,
        on_delete=models.PROTECT,                
        verbose_name="Mesa de Votación",
        help_text="Seleccione."
    )

    # Un votante puede tener un líder
    lider_asignado = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='votantes_asignados',
        limit_choices_to={'rol': 'LIDER_VOTANTE'},
        verbose_name="Líder Responsable"
    )

    status = models.CharField(
        max_length=8, 
        choices=STATUS_CHOICES, 
        default='ACTIVE',
        verbose_name='Estado',
        help_text="Estado actual (Activo/Inactivo)."
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        permissions = [
            ("change_status_votante", "Puede activar/inactivar votantes"),
        ]
        verbose_name = "votante"
        verbose_name_plural = "votantes"