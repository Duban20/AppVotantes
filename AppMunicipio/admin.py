from django.contrib import admin

from appcorregimientos.models import Corregimiento
from .models import Municipio

class CorregimientoInline(admin.TabularInline):
    model = Corregimiento
    extra = 1  # número de formularios vacíos que aparecerán por defecto
    autocomplete_fields = ('municipio',) 

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento')
    search_fields = ('nombre', 'departamento__nombre')
    ordering = ('nombre',)

    autocomplete_fields = ('departamento',)

    fieldsets = (
        ('Información del Municipio', {
            'fields': ('nombre', 'departamento'),
        }),
    )

    inlines = [CorregimientoInline]


admin.site.register(Municipio, MunicipioAdmin)
