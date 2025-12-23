from django.contrib import admin
from .models import Corregimiento

class CorregimientoAdmin(admin.ModelAdmin):

# ---------- LISTADO ----------
    list_display = (
        'nombre',
        'municipio',
        'get_departamento',
        'status',
    )

    list_filter = (
        'status',
        'municipio__departamento',
    )

    search_fields = (
        'nombre',
        'municipio__nombre',
        'municipio__departamento__nombre',
    )

    ordering = ('nombre',)

    autocomplete_fields = ('municipio',)

    # ---------- OPTIMIZACIÓN ----------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'municipio',
            'municipio__departamento',
        )

    # ---------- COLUMNAS PERSONALIZADAS ----------
    @admin.display(description='Departamento', ordering='municipio__departamento__nombre')
    def get_departamento(self, obj):
        return obj.municipio.departamento

    # ---------- FIELDSETS DINÁMICOS ----------
    def get_fieldsets(self, request, obj=None):
        if obj is None:
            # CREAR (sin estado)
            return (
                ('Información del Corregimiento', {
                    'fields': (
                        'nombre',
                        'municipio',
                    )
                }),
            )
        else:
            # EDITAR (con estado)
            return (
                ('Información del Corregimiento', {
                    'fields': (
                        'nombre',
                        'municipio',
                        'status',
                    )
                }),
            )


admin.site.register(Corregimiento, CorregimientoAdmin)
