from django.http import JsonResponse
from django.shortcuts import render

from AppMunicipio.models import Municipio

def cargar_municipios(request):
    departamento_id = request.GET.get('departamento_id')
    municipios = Municipio.objects.filter(departamento_id=departamento_id, status='ACTIVE').order_by('nombre')
    
    # Devolvemos una lista de diccionarios con id y nombre
    return JsonResponse(list(municipios.values('id', 'nombre')), safe=False)