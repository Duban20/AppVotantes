from django.db import models

from AppPuestoVotacion.models import PuestoVotacion

class Mesa(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]

    numero = models.PositiveIntegerField(
        verbose_name="Número", 
        help_text="Ingrese el número de la mesa."
        )
    
    puesto_votacion = models.ForeignKey(
        PuestoVotacion,
        on_delete=models.CASCADE,
        verbose_name="Puesto de Votación",
        help_text="Seleccione el puesto de votación correspondiente."
    )
    
    status = models.CharField(
        max_length=8, 
        choices=STATUS_CHOICES, 
        default='ACTIVE',
        verbose_name='Estado',
        help_text="Estado actual (Activo/Inactivo)."
    )

    def __str__(self):
        return f"Mesa {self.numero} - {self.puesto_votacion}"

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        constraints = [
        models.UniqueConstraint(
            fields=['numero', 'puesto_votacion'],
            name='unique_mesa_por_puesto'
            )
        ]