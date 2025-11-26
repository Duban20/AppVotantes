from django import forms
from .models import Municipio

class MunicipioForm(forms.ModelForm):
    class Meta:
        model = Municipio
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }