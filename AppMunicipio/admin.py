from django.contrib import admin
from .models import Municipio


class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento', 'status')
    search_fields = ('nombre', 'departamento__nombre')
    ordering = ('nombre',)

    fieldsets = (
        ('Información del Municipio / Corregimiento', {
            'fields': ('nombre', 'departamento', 'status'),
        }),
    )


admin.site.register(Municipio, MunicipioAdmin)
