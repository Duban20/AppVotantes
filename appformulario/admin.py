from django.contrib import admin
from .models import votante

class VotanteAdmin(admin.ModelAdmin):
    list_display = (
    'nombre', 'apellido', 'cedula', 
    'direccion_residencia',  
    'telefono',
    'lider_nombre',
    'mesa_numero',
    'puesto_direccion',
    'puesto_nombre',
    'municipio_y_departamento_puesto',
)


    # Filtros y búsqueda útiles
    list_filter = ('status', 'lider', 'mesa__puesto_votacion__municipio__departamento')
    search_fields = (
        'nombre', 'apellido', 'cedula', 'telefono',
        'lider__nombre', 'mesa__numero', 'mesa__puesto_votacion__nombre_lugar'
    )
    ordering = ('apellido', 'nombre')

    autocomplete_fields = ('mesa', 'lider')

    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'cedula', 'direccion_residencia', 'telefono')
        }),
        ('Datos Electorales', {
            'fields': ('lider', 'mesa',)
        }),
    )

    # -----------------------
    # MÉTODOS PARA CADA COLUMNA
    # -----------------------

    # LÍDER: solo nombre
    def lider_nombre(self, obj):
        return obj.lider.nombre if getattr(obj, 'lider', None) else '—'
    lider_nombre.short_description = 'Líder'
    lider_nombre.admin_order_field = 'lider__nombre'

    # MESA: solo número
    def mesa_numero(self, obj):
        return obj.mesa.numero if getattr(obj, 'mesa', None) else '—'
    mesa_numero.short_description = 'Mesa'
    mesa_numero.admin_order_field = 'mesa__numero'

    # PUESTO: dirección
    def puesto_direccion(self, obj):
        try:
            pv = obj.mesa.puesto_votacion
            # Si en tu modelo guardas "N/A" cuando no aplica, se mostrará eso
            return pv.direccion if pv else '—'
        except Exception:
            return '—'
    puesto_direccion.short_description = 'Dirección Puesto'
    puesto_direccion.admin_order_field = 'mesa__puesto_votacion__direccion'

    # PUESTO: nombre del puesto
    def puesto_nombre(self, obj):
        try:
            pv = obj.mesa.puesto_votacion
            return pv.nombre_lugar if pv else '—'
        except Exception:
            return '—'
    puesto_nombre.short_description = 'Puesto'
    puesto_nombre.admin_order_field = 'mesa__puesto_votacion__nombre_lugar'

    # MUNICIPIO & DEPARTAMENTO DEL PUESTO (juntos)
    def municipio_y_departamento_puesto(self, obj):
        try:
            municipio = obj.mesa.puesto_votacion.municipio
            if municipio:
                # Usamos los campos explícitos para evitar depender únicamente de __str__
                depto = municipio.departamento.nombre if municipio.departamento else ''
                return f"{municipio.nombre} – {depto}" if depto else municipio.nombre
            return '—'
        except Exception:
            return '—'
    municipio_y_departamento_puesto.short_description = 'Mun. – Departamento (Puesto)'
    municipio_y_departamento_puesto.admin_order_field = 'mesa__puesto_votacion__municipio__nombre'

# Registrar admin
admin.site.register(votante, VotanteAdmin)
