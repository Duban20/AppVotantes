from django import forms
from appmesa.models import Mesa
from AppPuestoVotacion.models import PuestoVotacion  
from .models import votante


class VotanteForm(forms.ModelForm):

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")

        # Si estás editando un votante, excluir ese mismo registro
        votante_id = self.instance.pk

        if votante.objects.filter(cedula=cedula).exclude(pk=votante_id).exists():
            raise forms.ValidationError("Esta cédula ya está registrada.")

        return cedula

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Select Puesto primero → solo puestos activos
        self.fields['puesto_votacion'].queryset = PuestoVotacion.objects.filter(
            status='ACTIVE'
        ).order_by('nombre_lugar')

        # Select Mesa se cargará dinámicamente → no mostrar mesas aún
        self.fields['mesa'].queryset = Mesa.objects.none()

        # Si estás editando un votante, cargar mesas correspondientes al puesto ya guardado
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


    class Meta:
        model = votante
        fields = [
            'nombre',
            'apellido',
            'cedula',
            'direccion_residencia',
            'telefono',
            'puesto_votacion',  
            'mesa',
            'lider'
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.NumberInput(attrs={'class': 'form-control'}),
            'direccion_residencia': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'puesto_votacion': forms.Select(attrs={'class': 'form-select'}),
            'mesa': forms.Select(attrs={'class': 'form-select'}),
            'lider': forms.Select(attrs={'class': 'form-select'}),
        }
