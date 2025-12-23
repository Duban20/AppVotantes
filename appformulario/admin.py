from django.contrib import admin
from .models import Votante


class VotanteAdmin(admin.ModelAdmin):

    # ---------- LISTADO ----------
    list_display = (
        'nombre',
        'apellido',
        'cedula',
        'direccion_residencia',
        'telefono',
        'rol',
        'lider_nombre',
        'lider_cedula',
        'lider_telefono',
        'mesa_numero',
        'puesto_direccion',
        'barrio_residencia',
        'puesto_nombre',
        'municipio_y_departamento_puesto',
        'status',
    )

    list_filter = (
        'status',
        'rol',
        'mesa__puesto_votacion__municipio__departamento',
        'mesa',
        'mesa__puesto_votacion',
    )

    search_fields = (
        'nombre',
        'apellido',
        'cedula',
        'telefono',
        'lider_asignado__nombre',
        'lider_asignado__apellido',
        'mesa__numero',
        'mesa__puesto_votacion__nombre_lugar',
    )

    ordering = ('apellido', 'nombre')

    autocomplete_fields = ('mesa', 'lider_asignado')

    # ---------- FIELDSETS ----------
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

    # ---------- OPTIMIZACIÓN ----------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'lider_asignado',
            'mesa',
            'mesa__puesto_votacion',
            'mesa__puesto_votacion__municipio',
            'mesa__puesto_votacion__municipio__departamento',
        )

    # ---------------------------------------------------
    # COLUMNAS PERSONALIZADAS
    # ---------------------------------------------------

    def lider_nombre(self, obj):
        if obj.lider_asignado:
            return f"{obj.lider_asignado.nombre} {obj.lider_asignado.apellido}"
        return "—"
    lider_nombre.short_description = "Líder"
    lider_nombre.admin_order_field = "lider_asignado__nombre"

    def lider_cedula(self, obj):
        return obj.lider_asignado.cedula if obj.lider_asignado else "—"
    lider_cedula.short_description = "Cédula Líder"

    def lider_telefono(self, obj):
        return obj.lider_asignado.telefono if obj.lider_asignado else "—"
    lider_telefono.short_description = "Teléfono Líder"

    def mesa_numero(self, obj):
        return obj.mesa.numero if obj.mesa else "—"
    mesa_numero.short_description = "Mesa"
    mesa_numero.admin_order_field = "mesa__numero"

    def puesto_direccion(self, obj):
        try:
            pv = obj.mesa.puesto_votacion
            return pv.direccion if pv else "—"
        except Exception:
            return "—"
    puesto_direccion.short_description = "Dirección Puesto"
    puesto_direccion.admin_order_field = "mesa__puesto_votacion__direccion"

    def puesto_nombre(self, obj):
        try:
            pv = obj.mesa.puesto_votacion
            return pv.nombre_lugar if pv else "—"
        except Exception:
            return "—"
    puesto_nombre.short_description = "Puesto"
    puesto_nombre.admin_order_field = "mesa__puesto_votacion__nombre_lugar"

    def municipio_y_departamento_puesto(self, obj):
        try:
            municipio = obj.mesa.puesto_votacion.municipio
            if municipio:
                depto = municipio.departamento.nombre if municipio.departamento else ''
                return f"{municipio.nombre} – {depto}" if depto else municipio.nombre
        except Exception:
            pass
        return "—"
    municipio_y_departamento_puesto.short_description = "Mun. – Departamento (Puesto)"
    municipio_y_departamento_puesto.admin_order_field = "mesa__puesto_votacion__municipio__nombre"


# Registrar admin
admin.site.register(Votante, VotanteAdmin)
