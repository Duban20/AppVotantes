from django.contrib import admin
from AppMunicipio.models import Municipio
from appdepartamento.models import Departamento

class MunicipioInline(admin.TabularInline):  
    model = Municipio
    extra = 1
    fields = ('nombre',)
    
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'status')
    list_filter = ('status',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

    # ---------- FIELDSETS DINÁMICOS ----------
    def get_fieldsets(self, request, obj=None):
        if obj is None:
            # CREAR (sin estado)
            return (
                ('Información de departamentos', {
                    'fields': ('nombre',)
                }),
            )
        else:
            # EDITAR (con estado)
            return (
                ('Información de departamentos', {
                    'fields': (
                        'nombre',
                        'status',
                    )
                }),
            )

    inlines = [MunicipioInline]

admin.site.register(Departamento, DepartamentoAdmin)
