from django.contrib import admin
from appdepartamento.models import Departamento

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'status')
    list_filter = ('nombre', 'status',)
    search_fields = ('nombre',)
    ordering = ('nombre',)
    
    fieldsets = (
        ('Información de departamentos', {
            'fields': ('nombre',)
        }),
    )


admin.site.register(Departamento, DepartamentoAdmin)
