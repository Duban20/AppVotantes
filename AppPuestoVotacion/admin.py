from django.contrib import admin
from django import forms
from django.db import transaction
from appmesa.models import Mesa
from .models import PuestoVotacion


class PuestoVotacionAdminForm(forms.ModelForm):
    cantidad_mesas = forms.IntegerField(
        label="Cantidad de mesas",
        min_value=1,
        required=False,
        help_text="Número de mesas que tendrá este puesto"
    )

    class Meta:
        model = PuestoVotacion
        fields = '__all__'

class MesaInline(admin.TabularInline):
    model = Mesa
    extra = 0
    fields = ('numero',)
    
class PuestoVotacionAdmin(admin.ModelAdmin):
    
    form = PuestoVotacionAdminForm 

    list_display = (
        'nombre_lugar',
        'departamento',
        'municipio',
        'corregimiento',
        'status',
    )

    list_filter = (
        'departamento',
        'municipio',
        'status',
    )

    search_fields = ('nombre_lugar',)
    ordering = ('nombre_lugar',)

    inlines = [MesaInline]

    # ---------- OPTIMIZACIÓN ----------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'municipio',
            'municipio__departamento',
            'corregimiento',
        )
    
    # ---------- COLUMNAS CALCULADAS ----------
    @admin.display(description='Departamento', ordering='municipio__departamento__nombre')
    def departamento(self, obj):
        return obj.municipio.departamento.nombre

    @admin.display(description='Municipio', ordering='municipio__nombre')
    def municipio(self, obj):
        return obj.municipio.nombre

    @admin.display(description='Corregimiento', ordering='corregimiento__nombre')
    def corregimiento(self, obj):
        return obj.corregimiento or '—'

    # autocomplete_fields = ('municipio',)

    # ---------- FIELDSETS DINÁMICOS ----------
    def get_fieldsets(self, request, obj=None):
        if obj is None:
            # CREAR
            return (
                ('Ubicación', {
                    'fields': (
                        'departamento',
                        'municipio',
                        'corregimiento',
                    )
                }),
                ('Información', {
                    'fields': (
                        'nombre_lugar',
                        'direccion',
                        'cantidad_mesas',
                    )
                }),
            )
        else:
            # EDITAR
            return (
                ('Ubicación', {
                    'fields': (
                        'departamento',
                        'municipio',
                        'corregimiento',
                    )
                }),
                ('Información', {
                    'fields': (
                        'nombre_lugar',
                        'direccion',
                        'status',
                    )
                }),
            )

    # ---------- MOSTRAR INLINES SOLO AL EDITAR ----------
    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)

    # ---------- GUARDADO Y CREACIÓN DE MESAS ----------
    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            super().save_model(request, obj, form, change)

            if not change:
                cantidad = form.cleaned_data.get('cantidad_mesas')
                if cantidad:
                    Mesa.objects.bulk_create([
                        Mesa(
                            puesto_votacion=obj,
                            numero=i + 1
                        )
                        for i in range(cantidad)
                    ])

admin.site.register(PuestoVotacion, PuestoVotacionAdmin)
