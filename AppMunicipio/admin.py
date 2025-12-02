from django.contrib import admin
from .models import Municipio


class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento')
    search_fields = ('nombre', 'departamento__nombre')
    ordering = ('nombre',)

    autocomplete_fields = ('departamento',)

    fieldsets = (
        ('Información del Municipio / Corregimiento', {
            'fields': ('nombre', 'departamento'),
        }),
    )


admin.site.register(Municipio, MunicipioAdmin)
