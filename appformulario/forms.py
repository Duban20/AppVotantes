from django import forms
from django.db import transaction
from appcorregimientos.models import Corregimiento
from appdepartamento.models import Departamento
from appmesa.models import Mesa
from AppPuestoVotacion.models import PuestoVotacion  
from AppMunicipio.models import Municipio
from .models import SubLider, Votante, LiderEG

class VotanteForm(forms.ModelForm):

    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")
        votante_id = self.instance.pk
        if Votante.objects.filter(cedula=cedula).exclude(pk=votante_id).exists():
            raise forms.ValidationError("Esta cédula ya está registrada.")
        return cedula
    
    def clean(self):
        cleaned_data = super().clean()
        rol = cleaned_data.get('rol')
        lider_eg = cleaned_data.get('lider_eg')
        sublider_asignado = cleaned_data.get('sublider')

        # --- VALIDACIONES DE ROL ---
        if rol == 'VOTANTE' and not lider_eg:
            raise forms.ValidationError("Un votante debe tener un Líder EG asignado.")

        if rol == 'SUBLIDER' and not lider_eg:
            raise forms.ValidationError("Un SubLíder debe tener un Líder EG asignado.")

        if rol == 'LIDER_EG' and lider_eg:
            raise forms.ValidationError("Un Líder EG no puede tener líder asignado.")
        
        # Validación lógica: No puedes asignar un sublíder si el rol es Líder o Sublíder
        if rol in ['LIDER_EG', 'SUBLIDER'] and sublider_asignado:
            cleaned_data['sublider'] = None # Limpiamos para evitar inconsistencias

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- FILTRO: LUGAR DE VOTACIÓN ---
        self.fields['puesto_votacion'].queryset = PuestoVotacion.objects.filter(
            status='ACTIVE'
        ).order_by('nombre_lugar')

        self.fields['mesa'].queryset = Mesa.objects.none()

        if "puesto_votacion" in self.data:
            try:
                puesto_id = int(self.data.get("puesto_votacion"))
                self.fields['mesa'].queryset = Mesa.objects.filter(
                    puesto_votacion_id=puesto_id, status='ACTIVE'
                ).order_by("numero")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.puesto_votacion:
            self.fields['mesa'].queryset = Mesa.objects.filter(
                puesto_votacion=self.instance.puesto_votacion, status='ACTIVE'
            ).order_by('numero')

        # --- FILTRO: LÍDER EG ---
        self.fields['lider_eg'].queryset = LiderEG.objects.filter(
            votante__status='ACTIVE'
        ).select_related('votante').order_by('votante__nombre')

        # --- FILTRO: SUBLÍDER (Depende de LIDER EG) ---
        self.fields['sublider'].queryset = SubLider.objects.none()

        if "lider_eg" in self.data:
            try:
                lider_id = int(self.data.get("lider_eg"))
                self.fields['sublider'].queryset = SubLider.objects.filter(
                    lider_eg_id=lider_id, votante__status='ACTIVE'
                ).select_related('votante').order_by('votante__nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.lider_eg:
            self.fields['sublider'].queryset = SubLider.objects.filter(
                lider_eg=self.instance.lider_eg, votante__status='ACTIVE'
            ).order_by('votante__nombre')

        # --- FILTRO: RESIDENCIA ---
        self.fields['departamento_residencia'].queryset = Departamento.objects.all().order_by('nombre')
        self.fields['municipio_residencia'].queryset = Municipio.objects.none()

        if 'departamento_residencia' in self.data:
            try:
                dep_id = int(self.data.get('departamento_residencia'))
                self.fields['municipio_residencia'].queryset = Municipio.objects.filter(departamento_id=dep_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.municipio_residencia:
            self.fields['municipio_residencia'].queryset = Municipio.objects.filter(
                departamento=self.instance.municipio_residencia.departamento
            ).order_by('nombre')

        self.fields['corregimiento_residencia'].queryset = Corregimiento.objects.none()
        if "municipio_residencia" in self.data:
            try:
                muni_id = int(self.data.get("municipio_residencia"))
                self.fields['corregimiento_residencia'].queryset = Corregimiento.objects.filter(
                    municipio_id=muni_id, status='ACTIVE'
                ).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.corregimiento_residencia:
            self.fields['corregimiento_residencia'].queryset = Corregimiento.objects.filter(
                municipio=self.instance.corregimiento_residencia.municipio, status='ACTIVE'
            ).order_by('nombre')

    def save(self, commit=True):
        with transaction.atomic():
            votante = super().save(commit=commit)
            rol = self.cleaned_data.get('rol')
            lider_eg_asignado = self.cleaned_data.get('lider_eg')

            if rol == 'LIDER_EG':
                # Crear perfil de Líder y borrar si era Sublíder
                LiderEG.objects.get_or_create(votante=votante)
                SubLider.objects.filter(votante=votante).delete()

            elif rol == 'SUBLIDER':
                # Crear perfil de Sublíder vinculado al Líder y borrar si era Líder EG
                if lider_eg_asignado:
                    SubLider.objects.update_or_create(
                        votante=votante,
                        defaults={'lider_eg': lider_eg_asignado}
                    )
                LiderEG.objects.filter(votante=votante).delete()
            
            else:
                # Si el rol baja a VOTANTE, se eliminan sus privilegios de mando
                LiderEG.objects.filter(votante=votante).delete()
                SubLider.objects.filter(votante=votante).delete()

            return votante

    class Meta:
        model = Votante
        fields = [
            'rol', 'nombre', 'apellido', 'cedula',
            'departamento_residencia', 'municipio_residencia', 'corregimiento_residencia',
            'direccion_residencia', 'barrio_residencia', 'telefono',
            'puesto_votacion', 'mesa', 'lider_eg', 'sublider'
        ]

        widgets = {
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombres','class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellidos','class': 'form-control'}),
            'cedula': forms.NumberInput(attrs={'placeholder': 'Cédula','class': 'form-control'}),
            'departamento_residencia': forms.Select(attrs={'class': 'form-select'}),
            'municipio_residencia': forms.Select(attrs={'class': 'form-select'}),
            'corregimiento_residencia': forms.Select(attrs={'class': 'form-select'}),
            'direccion_residencia': forms.TextInput(attrs={'placeholder': 'Dirección','class': 'form-control'}),
            'barrio_residencia': forms.TextInput(attrs={'placeholder': 'Barrio','class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'placeholder': 'Teléfono','class': 'form-control'}),
            'puesto_votacion': forms.Select(attrs={'class': 'form-select'}),
            'mesa': forms.Select(attrs={'class': 'form-select'}),
            'lider_eg': forms.Select(attrs={'class': 'form-select'}),
            'sublider': forms.Select(attrs={'class': 'form-select'}),
        }