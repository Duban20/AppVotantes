from django.contrib import admin
from appmesa.models import Mesa

class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'puesto_votacion',)
    list_filter = ('puesto_votacion', 'status')
    search_fields = ('numero', 
                     'puesto_votacion__nombre_lugar',    
                     'puesto_votacion__municipio__nombre',
                     'puesto_votacion__municipio__departamento__nombre',
                    )
    ordering = ('numero',)
    list_filter = ('status',)

    autocomplete_fields = ('puesto_votacion',)

    fieldsets = (
        ('Información de Mesas', {
            'fields': ('numero', 'puesto_votacion'),
        }),
    )


admin.site.register(Mesa, MesaAdmin)
