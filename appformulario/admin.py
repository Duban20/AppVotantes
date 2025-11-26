from django.contrib import admin
from .models import votante

class VotanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'telefono', 'edad', 'puesto_votacion', 'lider', 'municipio_nacimiento', 'status')
    list_filter = ('status', 'puesto_votacion', 'municipio_nacimiento', 'lider')
    search_fields = ('nombre', 'apellido', 'cedula', 'telefono', 'municipio_nacimiento', 'lider')
    ordering = ('apellido', 'nombre')

    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'cedula', 'edad', 'telefono')
        }),
        ('Datos Electorales', {
            'fields': ('puesto_votacion', 'lider', 'municipio_nacimiento')
        }),
        ('Estado del Registro', {
            'fields': ('status',)
        }),
    )

admin.site.register(votante, VotanteAdmin)
