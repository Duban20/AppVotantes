from django.db import models

class Lider(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Activo'),
        ('INACTIVE', 'Inactivo'),
    ]

    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre del líder",
        help_text="Ingrese el nombre completo del líder."
    )

    cedula = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Cédula",
        help_text="Número de identificación del líder."
    )

    telefono = models.CharField(
        max_length=12,
        verbose_name="Teléfono",
        blank=True, null=True,
        help_text="Número de contacto del líder."
    )

    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        verbose_name="Estado",
        help_text="Estado actual (Activo/Inactivo)."
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Líder"
        verbose_name_plural = "Líderes"
