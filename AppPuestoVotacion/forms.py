from django import forms

from AppMunicipio.models import Municipio
from .models import PuestoVotacion

class PuestoVotacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicar filtro para Municipios (solo ACTIVO)
        self.fields['municipio'].queryset = Municipio.objects.filter(
            status='ACTIVE'
        ).order_by('nombre')
        
    class Meta:
        model = PuestoVotacion
        fields = ['nombre_lugar', 'aplica_direccion', 'direccion', 'municipio']
        widgets = {
            'nombre_lugar': forms.TextInput(attrs={'class': 'form-control'}),
            'aplica_direccion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.Select(attrs={'class': 'form-select'}),
        }
