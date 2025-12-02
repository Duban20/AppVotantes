from django.contrib import admin
from AppMunicipio.models import Municipio
from appdepartamento.models import Departamento

class MunicipioInline(admin.TabularInline):  
    model = Municipio
    extra = 1
    fields = ('nombre',)
    
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ('status',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

    fieldsets = (
        ('Información de departamentos', {
            'fields': ('nombre',)
        }),
    )

    inlines = [MunicipioInline]

    # Filtrar solo departamentos activos 
    def get_queryset(self, request):
        return Departamento.objects.filter(status='ACTIVE')


admin.site.register(Departamento, DepartamentoAdmin)
