from django.contrib import admin
from .models import Municipio


class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

    fieldsets = (
        ('Información del Municipio / Corregimiento', {
            'fields': ('nombre',)
        }),
    )


admin.site.register(Municipio, MunicipioAdmin)
