from django.shortcuts import render

from AppMunicipio.models import Municipio
from AppPuestoVotacion.models import PuestoVotacion
from appformulario.models import votante 

def home(request):
    # Conteos de registros
    try:
        total_votantes = votante.objects.count()
        total_puestos = PuestoVotacion.objects.count()
        total_municipios = Municipio.objects.count()
    except Exception as e:
        # Manejo de error si la BD no está disponible
        print(f"Error al contar registros: {e}")
        total_votantes = 0
        total_puestos = 0
        total_municipios = 0


    # Diccionario de contexto para la plantilla
    context = {
        'total_votantes': total_votantes,
        'total_puestos': total_puestos,
        'total_municipios': total_municipios,
    }
    
    # Renderizar la plantilla
    return render(request, 'home.html', context)