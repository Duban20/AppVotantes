from django.contrib import admin
from appmesa.models import Mesa

class MesaAdmin(admin.ModelAdmin):

    list_display = (
        'numero',
        'puesto',
        'departamento',
        'municipio',
        'corregimiento',
        'status',
    )

    list_filter = (
        'puesto_votacion__municipio__departamento',
        'puesto_votacion__municipio',
        'status',
    )

    search_fields = (
        'numero',
        'puesto_votacion__nombre_lugar',
        'puesto_votacion__municipio__nombre',
        'puesto_votacion__municipio__departamento__nombre',
    )

    ordering = ('puesto_votacion', 'numero')

    autocomplete_fields = ('puesto_votacion',)

    # ---------- FIELDSETS DINÁMICOS ----------
    def get_fieldsets(self, request, obj=None):
        if obj is None:
            # CREAR (sin estado)
            return (
                ('Información de Mesas', {
                    'fields': (
                        'numero',
                        'puesto_votacion',
                    ),
                }),
            )
        else:
            # EDITAR (con estado)
            return (
                ('Información de Mesas', {
                    'fields': (
                        'numero',
                        'puesto_votacion',
                        'status',
                    ),
                }),
            )

     # ---------- OPTIMIZACIÓN ----------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'puesto_votacion',
            'puesto_votacion__municipio',
            'puesto_votacion__municipio__departamento',
            'puesto_votacion__corregimiento',
        )

    # ---------- COLUMNAS ----------
    @admin.display(description='Puesto')
    def puesto(self, obj):
        return obj.puesto_votacion.nombre_lugar

    @admin.display(description='Departamento')
    def departamento(self, obj):
        return obj.puesto_votacion.municipio.departamento.nombre

    @admin.display(description='Municipio')
    def municipio(self, obj):
        return obj.puesto_votacion.municipio.nombre

    @admin.display(description='Corregimiento')
    def corregimiento(self, obj):
        return obj.puesto_votacion.corregimiento or '—'

admin.site.register(Mesa, MesaAdmin)
