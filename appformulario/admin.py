from django.contrib import admin
from django.db.models import Count
from simple_history.admin import SimpleHistoryAdmin
from .models import LiderEG, SubLider, Votante

# --------------------------------------------------
# FILTROS PERSONALIZADOS
# --------------------------------------------------

class VotantesPorLiderFilter(admin.SimpleListFilter):
    title = 'Votantes por Líder EG'
    parameter_name = 'lider_eg_id'

    def lookups(self, request, model_admin):
        # Solo mostrar líderes que tienen votantes asignados
        lideres = LiderEG.objects.annotate(total=Count('votantes')).filter(total__gt=0)
        return [(l.id, f"{l.votante.nombre} {l.votante.apellido} ({l.total})") for l in lideres]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(lider_eg_id=self.value())
        return queryset

class VotantesPorSubliderFilter(admin.SimpleListFilter):
    title = 'Votantes por Sublíder'
    parameter_name = 'sublider_id'

    def lookups(self, request, model_admin):
        sublideres = SubLider.objects.annotate(total=Count('votantes')).filter(total__gt=0)
        return [(s.id, f"{s.votante.nombre} {s.votante.apellido} ({s.total})") for s in sublideres]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(sublider_id=self.value())
        return queryset

# --------------------------------------------------
# ADMIN DE VOTANTE
# --------------------------------------------------

@admin.register(Votante)
class VotanteAdmin(SimpleHistoryAdmin):
    # Listado principal
    list_display = (
        'nombre', 'apellido', 'cedula', 'rol', 
        'get_superior', 'puesto_nombre', 'status'
    )
    
    list_filter = (
        'rol',
        'status',
        VotantesPorLiderFilter,
        VotantesPorSubliderFilter,
        'puesto_votacion__municipio__departamento',
        'puesto_votacion__municipio',
    )

    search_fields = (
        'nombre', 'apellido', 'cedula', 'telefono',
        'lider_eg__votante__nombre', 'lider_eg__votante__apellido',
        'sublider__votante__nombre', 'sublider__votante__apellido',
        'puesto_votacion__nombre_lugar',
    )

    autocomplete_fields = ('puesto_votacion', 'lider_eg', 'sublider')
    
    ordering = ('apellido', 'nombre')

    # Organización del formulario
    fieldsets = (
        ('Jerarquía y Rol', {
            'fields': ('rol', 'lider_eg', 'sublider', 'status')
        }),
        ('Información Personal', {
            'fields': (
                ('nombre', 'apellido'),
                'cedula',
                'telefono',
                ('municipio_residencia', 'barrio_residencia'),
                'direccion_residencia',
            )
        }),
        ('Datos Electorales', {
            'fields': (
                'puesto_votacion',
                'mesa',
                'motivo_inactivacion',
            )
        }),
    )

    # Optimization
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'lider_eg__votante', 
            'sublider__votante', 
            'puesto_votacion__municipio__departamento'
        )

    # Columnas personalizadas
    @admin.display(description="Superior (Líder/Sub)")
    def get_superior(self, obj):
        if obj.sublider:
            return f"S: {obj.sublider.votante.nombre}"
        if obj.lider_eg:
            return f"L: {obj.lider_eg.votante.nombre}"
        return "—"

    @admin.display(description="Puesto", ordering="puesto_votacion__nombre_lugar")
    def puesto_nombre(self, obj):
        return obj.puesto_votacion.nombre_lugar if obj.puesto_votacion else "—"

    # Lógica de guardado automática
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # 1. Si es LIDER_EG, asegurar que exista en la tabla LiderEG
        if obj.rol == 'LIDER_EG':
            LiderEG.objects.get_or_create(votante=obj)
            # Si era sublíder antes, borrar ese perfil
            SubLider.objects.filter(votante=obj).delete()
            
        # 2. Si es SUBLIDER, asegurar que exista en la tabla SubLider
        elif obj.rol == 'SUBLIDER':
            # Nota: Aquí se creará, pero el usuario deberá asignar el lider_eg 
            # manualmente en la tabla SubLider o puedes pedirlo aquí.
            SubLider.objects.get_or_create(votante=obj, defaults={'lider_eg': obj.lider_eg})
            LiderEG.objects.filter(votante=obj).delete()
            
        # 3. Si es VOTANTE raso, eliminar cualquier perfil de mando
        else:
            LiderEG.objects.filter(votante=obj).delete()
            SubLider.objects.filter(votante=obj).delete()

# --------------------------------------------------
# ADMIN DE MANDO (LiderEG y SubLider)
# --------------------------------------------------

@admin.register(LiderEG)
class LiderEGAdmin(admin.ModelAdmin):
    list_display = ('get_nombre', 'get_cedula', 'total_sublideres', 'total_votantes')
    search_fields = ('votante__nombre', 'votante__apellido', 'votante__cedula')
    
    def get_nombre(self, obj): return f"{obj.votante.nombre} {obj.votante.apellido}"
    get_nombre.short_description = "Líder"

    def get_cedula(self, obj): return obj.votante.cedula
    get_cedula.short_description = "Cédula"

    def total_sublideres(self, obj): return obj.sublideres.count()
    total_sublideres.short_description = "Sublíderes"

    def total_votantes(self, obj): return obj.votantes.count()
    total_votantes.short_description = "Votantes Directos"

@admin.register(SubLider)
class SubLiderAdmin(admin.ModelAdmin):
    list_display = ('get_nombre', 'lider_eg', 'total_votantes')
    list_filter = ('lider_eg',)
    search_fields = ('votante__nombre', 'votante__apellido', 'votante__cedula')
    autocomplete_fields = ('lider_eg', 'votante')

    def get_nombre(self, obj): return f"{obj.votante.nombre} {obj.votante.apellido}"
    get_nombre.short_description = "Sublíder"

    def total_votantes(self, obj): return obj.votantes.count()
    total_votantes.short_description = "Votantes a Cargo"