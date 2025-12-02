from django.contrib import admin

from appmesa.models import Mesa
from .models import PuestoVotacion

class MesaInline(admin.TabularInline): 
    model = Mesa
    extra = 1
    fields = ('numero',)
    
class PuestoVotacionAdmin(admin.ModelAdmin):
    list_display = ('nombre_lugar', 'direccion', 'municipio')
    list_filter = ('municipio', 'status')
    search_fields = ('nombre_lugar', 'municipio__nombre')
    ordering = ('nombre_lugar',)

    autocomplete_fields = ('municipio',)

    fieldsets = (
        ('Información del Puesto de Votación', {
            'fields': (
                'nombre_lugar',
                'direccion',
                'municipio'
            )
        }),
    )

    inlines = [MesaInline]

admin.site.register(PuestoVotacion, PuestoVotacionAdmin)
