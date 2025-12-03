from django.contrib import admin
from .models import votante


class VotanteAdmin(admin.ModelAdmin):

    # Columnas visibles en la tabla del admin
    list_display = (
        'nombre',
        'apellido',
        'cedula',
        'direccion_residencia',
        'telefono',
        'rol',
        'lider_nombre',
        'mesa_numero',
        'puesto_direccion',
        'barrio_residencia',
        'puesto_nombre',
        'municipio_y_departamento_puesto',
        'status',
    )

    # Filtros
    list_filter = (
        'status',
        'rol',
        'mesa__puesto_votacion__municipio__departamento',
        'mesa',
        'mesa__puesto_votacion',
    )

    # Campos de búsqueda
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

    # Autocomplete
    autocomplete_fields = ('mesa', 'lider_asignado')

    # Fieldsets organizados
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

    # ---------------------------------------------------
    # MÉTODOS PERSONALIZADOS PARA COLUMNAS DEL ADMIN
    # ---------------------------------------------------

    def lider_nombre(self, obj):
        """Devuelve el nombre del líder asignado."""
        if obj.lider_asignado:
            return f"{obj.lider_asignado.nombre} {obj.lider_asignado.apellido}"
        return "—"
    lider_nombre.short_description = "Líder"
    lider_nombre.admin_order_field = "lider_asignado__nombre"

    def mesa_numero(self, obj):
        """Número de mesa."""
        return obj.mesa.numero if obj.mesa else "—"
    mesa_numero.short_description = "Mesa"
    mesa_numero.admin_order_field = "mesa__numero"

    def puesto_direccion(self, obj):
        """Dirección del puesto de votación."""
        try:
            pv = obj.mesa.puesto_votacion
            return pv.direccion if pv else "—"
        except:
            return "—"
    puesto_direccion.short_description = "Dirección Puesto"
    puesto_direccion.admin_order_field = "mesa__puesto_votacion__direccion"

    def puesto_nombre(self, obj):
        """Nombre del puesto."""
        try:
            pv = obj.mesa.puesto_votacion
            return pv.nombre_lugar if pv else "—"
        except:
            return "—"
    puesto_nombre.short_description = "Puesto"
    puesto_nombre.admin_order_field = "mesa__puesto_votacion__nombre_lugar"

    def municipio_y_departamento_puesto(self, obj):
        """Municipio y departamento del puesto."""
        try:
            municipio = obj.mesa.puesto_votacion.municipio
            if municipio:
                depto = municipio.departamento.nombre if municipio.departamento else ''
                return f"{municipio.nombre} – {depto}" if depto else municipio.nombre
        except:
            pass
        return "—"
    municipio_y_departamento_puesto.short_description = "Mun. – Departamento (Puesto)"
    municipio_y_departamento_puesto.admin_order_field = "mesa__puesto_votacion__municipio__nombre"

    # Filtro personalizado para puesto (porque no es FK directo)
    def puesto_votacion_filtro(self, obj):
        return obj.mesa.puesto_votacion.nombre_lugar if obj.mesa else "—"
    puesto_votacion_filtro.short_description = "Puesto de Votación"


# Registrar admin
admin.site.register(votante, VotanteAdmin)
