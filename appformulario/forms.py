from django import forms
from appcorregimientos.models import Corregimiento
from appdepartamento.models import Departamento
from appmesa.models import Mesa
from AppPuestoVotacion.models import PuestoVotacion  
from AppMunicipio.models import Municipio
from .models import Votante


class VotanteForm(forms.ModelForm):

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")

        # Si estás editando un votante, excluir ese mismo registro
        votante_id = self.instance.pk

        if Votante.objects.filter(cedula=cedula).exclude(pk=votante_id).exists():
            raise forms.ValidationError("Esta cédula ya está registrada.")

        return cedula

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- Puesto de votación (solo activos) ---
        self.fields['puesto_votacion'].queryset = PuestoVotacion.objects.filter(
            status='ACTIVE'
        ).order_by('nombre_lugar')

        # --- Mesa depende del puesto (dinámico) ---
        self.fields['mesa'].queryset = Mesa.objects.none()

        if "puesto_votacion" in self.data:
            try:
                puesto_id = int(self.data.get("puesto_votacion"))
                self.fields['mesa'].queryset = Mesa.objects.filter(
                    puesto_votacion_id=puesto_id,
                    status='ACTIVE'
                ).order_by("numero")
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            # Caso edición
            self.fields['mesa'].queryset = Mesa.objects.filter(
                puesto_votacion=self.instance.mesa.puesto_votacion,
                status='ACTIVE'
            ).order_by('numero')

        # --- LÍDER ASIGNADO ---
        # Mostrar solo líderes (rol = LIDER_VOTANTE)
        self.fields['lider_asignado'].queryset = Votante.objects.filter(
            rol='LIDER_VOTANTE',
            status='ACTIVE'
        ).order_by('nombre', 'apellido')

        # --- DEPARTAMENTO ---
        self.fields['departamento_residencia'].queryset = Departamento.objects.all().order_by('nombre')
        self.fields['departamento_residencia'].required = False

        # --- MUNICIPIO depende del departamento ---
        self.fields['municipio_residencia'].queryset = Municipio.objects.none()
        if 'departamento_residencia' in self.data:
            try:
                departamento_id = int(self.data.get('departamento_residencia'))
                self.fields['municipio_residencia'].queryset = Municipio.objects.filter(
                    departamento_id=departamento_id
                ).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.municipio_residencia:
            self.fields['municipio_residencia'].queryset = Municipio.objects.filter(
                departamento=self.instance.municipio_residencia.departamento
            ).order_by('nombre')

        # --- CORREGIMIENTO (depende del municipio seleccionado) ---
        self.fields['corregimiento_residencia'].queryset = Corregimiento.objects.none()
        if "municipio_residencia" in self.data:
            try:
                municipio_id = int(self.data.get("municipio_residencia"))
                self.fields['corregimiento_residencia'].queryset = Corregimiento.objects.filter(
                    municipio_id=municipio_id,
                    status='ACTIVE'
                ).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.corregimiento_residencia:
            self.fields['corregimiento_residencia'].queryset = Corregimiento.objects.filter(
                municipio=self.instance.corregimiento_residencia.municipio,
                status='ACTIVE'
            ).order_by('nombre')


    class Meta:
        model = Votante
        fields = [
            'rol',
            'nombre',
            'apellido',
            'cedula',
            'departamento_residencia',
            'municipio_residencia',
            'corregimiento_residencia',
            'direccion_residencia',
            'barrio_residencia',
            'telefono',
            'puesto_votacion',  
            'mesa',
            'lider_asignado',
        ]

        widgets = {
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.NumberInput(attrs={'class': 'form-control'}),
            'departamento_residencia': forms.Select(attrs={'class': 'form-select'}),
            'municipio_residencia': forms.Select(attrs={'class': 'form-select'}),
            'corregimiento_residencia': forms.Select(attrs={'class': 'form-select'}),
            'direccion_residencia': forms.TextInput(attrs={'class': 'form-control'}),
            'barrio_residencia': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'puesto_votacion': forms.Select(attrs={'class': 'form-select'}),
            'mesa': forms.Select(attrs={'class': 'form-select'}),
            'lider_asignado': forms.Select(attrs={'class': 'form-select'}),
        }
