from django.contrib import admin
from appmesa.models import Mesa

class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'puesto_votacion', 'status')
    list_filter = ('puesto_votacion', 'status')
    search_fields = ('numero',)
    ordering = ('numero',)
    list_filter = ('status',)

    fieldsets = (
        ('Información de Mesas', {
            'fields': ('numero', 'puesto_votacion', 'status'),
        }),
    )


admin.site.register(Mesa, MesaAdmin)
