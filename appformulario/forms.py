from django import forms

from AppMunicipio.models import Municipio
from AppPuestoVotacion.models import PuestoVotacion
from .models import votante

class VotanteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. Aplicar filtro para Puestos de Votación (solo ACTIVO)
        self.fields['puesto_votacion'].queryset = PuestoVotacion.objects.filter(
            status='ACTIVE'
        ).order_by('nombre_lugar')

        # 2. Aplicar filtro para Municipios (solo ACTIVO)
        self.fields['municipio_nacimiento'].queryset = Municipio.objects.filter(
            status='ACTIVE'
        ).order_by('nombre')
        
    class Meta:
        model = votante
        fields = [
            'nombre', 'apellido', 'cedula', 'edad', 'telefono',
            'puesto_votacion', 'lider', 'municipio_nacimiento'
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'puesto_votacion': forms.Select(attrs={'class': 'form-select'}),
            'lider': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio_nacimiento': forms.Select(attrs={'class': 'form-select'}),
        }