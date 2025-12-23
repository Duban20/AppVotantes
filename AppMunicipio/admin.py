from django.contrib import admin

from appcorregimientos.models import Corregimiento
from .models import Municipio

class CorregimientoInline(admin.TabularInline):
    model = Corregimiento
    extra = 1  # número de formularios vacíos que aparecerán por defecto
    autocomplete_fields = ('municipio',) 

class MunicipioAdmin(admin.ModelAdmin):
    
     # ---------- LISTADO ----------
    list_display = (
        'nombre',
        'departamento',
        'status',
    )

    list_filter = (
        'departamento',
        'status',
    )

    search_fields = (
        'nombre',
        'departamento__nombre',
    )

    ordering = ('nombre',)

    autocomplete_fields = ('departamento',)

    inlines = [CorregimientoInline]

    # ---------- OPTIMIZACIÓN ----------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('departamento')

    # ---------- FIELDSETS DINÁMICOS ----------
    def get_fieldsets(self, request, obj=None):
        if obj is None:
            # CREAR (sin estado)
            return (
                ('Información del Municipio', {
                    'fields': (
                        'nombre',
                        'departamento',
                    )
                }),
            )
        else:
            # EDITAR (con estado)
            return (
                ('Información del Municipio', {
                    'fields': (
                        'nombre',
                        'departamento',
                        'status',
                    )
                }),
            )

admin.site.register(Municipio, MunicipioAdmin)
