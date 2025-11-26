from django.contrib import admin
from .models import PuestoVotacion

class PuestoVotacionAdmin(admin.ModelAdmin):
    list_display = ('nombre_lugar', 'direccion', 'aplica_direccion', 'municipio')
    list_filter = ('municipio', 'aplica_direccion')
    search_fields = ('nombre_lugar', 'direccion', 'municipio__nombre')
    ordering = ('nombre_lugar',)

    fieldsets = (
        ('Información del Puesto de Votación', {
            'fields': (
                'nombre_lugar',
                'aplica_direccion',
                'direccion',
                'municipio',
            )
        }),
    )

    class Media:
        js = ('js/puesto_votacion.js',) 

admin.site.register(PuestoVotacion, PuestoVotacionAdmin)
