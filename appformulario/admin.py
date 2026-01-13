from django.contrib import admin
from django.db.models import Count
from simple_history.admin import SimpleHistoryAdmin
from .models import Votante


class VotantesPorLiderFilter(admin.SimpleListFilter):
    title = 'Votantes por líder'
    parameter_name = 'lider'

    def lookups(self, request, model_admin):
        lideres = (
            Votante.objects
            .filter(rol='LIDER_VOTANTE')
            .annotate(total=Count('votantes_asignados'))
            .filter(total__gt=0)
        )
        return [
            (lider.id, f"{lider.nombre} {lider.apellido} ({lider.total})")
            for lider in lideres
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                rol='VOTANTE',
                lider_asignado_id=self.value()
            )
        return queryset.filter(rol='VOTANTE')


class VotanteAdmin(SimpleHistoryAdmin):

    # --------------------------------------------------
    # LISTADO
    # --------------------------------------------------
    list_display = (
        'nombre',
        'apellido',
        'cedula',
        'telefono',
        'rol',
        'lider_nombre',
        'lider_cedula',
        'lider_telefono',
        'puesto_nombre',
        'puesto_direccion',
        'municipio_y_departamento_puesto',
        'status',
    )

    # --------------------------------------------------
    # FILTROS
    # --------------------------------------------------
    list_filter = (
        'status',
        VotantesPorLiderFilter,
        'puesto_votacion__departamento',
        'puesto_votacion',
    )

    # --------------------------------------------------
    # BÚSQUEDA
    # --------------------------------------------------
    search_fields = (
        'nombre',
        'apellido',
        'cedula',
        'telefono',
        'lider_asignado__nombre',
        'lider_asignado__apellido',
        'puesto_votacion__nombre_lugar',
        'puesto_votacion__direccion',
    )

    ordering = ('apellido', 'nombre')

    autocomplete_fields = (
        'lider_asignado',
        'puesto_votacion',
    )

    # --------------------------------------------------
    # FORMULARIO
    # --------------------------------------------------
    fieldsets = (
        ('Información Personal', {
            'fields': (
                'rol',
                'nombre',
                'apellido',
                'cedula',
                'municipio_residencia',
                'direccion_residencia',
                'barrio_residencia',
                'telefono',
            )
        }),
        ('Datos Electorales', {
            'fields': (
                'lider_asignado',
                'puesto_votacion',
                'mesa',
                'status',
            )
        }),
    )

    # --------------------------------------------------
    # OPTIMIZACIÓN
    # --------------------------------------------------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'lider_asignado',
            'puesto_votacion',
            'puesto_votacion__municipio',
            'puesto_votacion__municipio__departamento',
        )

    # --------------------------------------------------
    # COLUMNAS PERSONALIZADAS
    # --------------------------------------------------
    def lider_nombre(self, obj):
        return (
            f"{obj.lider_asignado.nombre} {obj.lider_asignado.apellido}"
            if obj.lider_asignado else "—"
        )
    lider_nombre.short_description = "Líder"
    lider_nombre.admin_order_field = "lider_asignado__nombre"

    def lider_cedula(self, obj):
        return obj.lider_asignado.cedula if obj.lider_asignado else "—"
    lider_cedula.short_description = "Cédula Líder"

    def lider_telefono(self, obj):
        return obj.lider_asignado.telefono if obj.lider_asignado else "—"
    lider_telefono.short_description = "Teléfono Líder"

    def puesto_nombre(self, obj):
        return obj.puesto_votacion.nombre_lugar if obj.puesto_votacion else "—"
    puesto_nombre.short_description = "Puesto"
    puesto_nombre.admin_order_field = "puesto_votacion__nombre_lugar"

    def puesto_direccion(self, obj):
        return obj.puesto_votacion.direccion if obj.puesto_votacion else "—"
    puesto_direccion.short_description = "Dirección Puesto"
    puesto_direccion.admin_order_field = "puesto_votacion__direccion"

    def municipio_y_departamento_puesto(self, obj):
        try:
            municipio = obj.puesto_votacion.municipio
            if municipio:
                depto = municipio.departamento.nombre if municipio.departamento else ''
                return f"{municipio.nombre} – {depto}" if depto else municipio.nombre
        except Exception:
            pass
        return "—"
    municipio_y_departamento_puesto.short_description = "Mun. – Departamento (Puesto)"
    municipio_y_departamento_puesto.admin_order_field = "puesto_votacion__municipio__nombre"


admin.site.register(Votante, VotanteAdmin)
