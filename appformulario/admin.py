from django.contrib import admin
from .models import votante

class VotanteAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'apellido',
        'cedula',
        'edad',
        'telefono',

        # Líder (solo nombre)
        'lider_nombre',

        # Mesa (solo número)
        'mesa_numero',

        # Puesto: dirección y nombre
        'puesto_direccion',
        'puesto_nombre',

        # Municipio y departamento del puesto (juntos)
        'municipio_y_departamento_puesto',

        # Municipio y departamento de nacimiento del votante (juntos)
        'municipio_y_departamento_nacimiento',

        # Estado (mantenerlo al final)
        'status',
    )

    # Filtros y búsqueda útiles
    list_filter = ('status', 'lider', 'mesa__puesto_votacion__municipio__departamento')
    search_fields = (
        'nombre', 'apellido', 'cedula', 'telefono',
        'lider__nombre', 'mesa__numero', 'mesa__puesto_votacion__nombre_lugar'
    )
    ordering = ('apellido', 'nombre')

    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'cedula', 'edad', 'telefono')
        }),
        ('Datos Electorales', {
            'fields': ('mesa', 'lider', 'municipio_nacimiento')
        }),
        ('Estado del Registro', {
            'fields': ('status',)
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

    # MUNICIPIO & DEPARTAMENTO DE NACIMIENTO (juntos)
    def municipio_y_departamento_nacimiento(self, obj):
        try:
            municipio = obj.municipio_nacimiento
            if municipio:
                depto = municipio.departamento.nombre if municipio.departamento else ''
                return f"{municipio.nombre} – {depto}" if depto else municipio.nombre
            return '—'
        except Exception:
            return '—'
    municipio_y_departamento_nacimiento.short_description = 'Mun. – Departamento (Nacimiento)'
    municipio_y_departamento_nacimiento.admin_order_field = 'municipio_nacimiento__nombre'


# Registrar admin
admin.site.register(votante, VotanteAdmin)
