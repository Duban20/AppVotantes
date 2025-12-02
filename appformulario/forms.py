from django import forms

from AppMunicipio.models import Municipio
from appmesa.models import Mesa
from .models import votante

class VotanteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. Filtrar Mesas activas
        self.fields['mesa'].queryset = Mesa.objects.filter(
            status='ACTIVE'
        ).order_by('numero')

        # 2. Filtrar Municipios activos
        self.fields['municipio_nacimiento'].queryset = Municipio.objects.filter(
            status='ACTIVE'
        ).order_by('nombre')

    class Meta:
        model = votante
        fields = [
            'nombre', 'apellido', 'cedula', 'direccion_residencia', 'telefono',
            'mesa', 'lider', 'municipio_nacimiento'
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_residencia': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'mesa': forms.Select(attrs={'class': 'form-select'}),
            'lider': forms.Select(attrs={'class': 'form-select'}), 
            'municipio_nacimiento': forms.Select(attrs={'class': 'form-select'}),
        }
