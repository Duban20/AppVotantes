from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError, Q
from django.contrib import messages
from .forms import MunicipioForm
from .models import Municipio

@login_required
@permission_required('AppMunicipio.view_municipio', raise_exception=True)
def lista_municipios(request):
    # 1. Obtener parámetros de búsqueda y filtro
    query = request.GET.get('q')
    status_filter = request.GET.get('status')
    
    municipios = Municipio.objects.all()

    # 2. Aplicar Búsqueda (filtrar por nombre)
    if query:
        municipios = municipios.filter(
            Q(nombre__icontains=query)
        )
    
    # 3. Aplicar Filtro por Estado (ACTIVE o INACTIVE)
    if status_filter in ['ACTIVE', 'INACTIVE']:
        municipios = municipios.filter(status=status_filter)
    
    # Ordenar 
    municipios = municipios.order_by('nombre')
        
    return render(request, 'municipio/lista.html', {
        'municipios': municipios,
        'query': query,
        'status_filter': status_filter,
    })

@login_required
@permission_required('AppMunicipio.add_municipio', raise_exception=True)
def crear_municipio(request):
    if request.method == 'POST':
        form = MunicipioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Municipio/Corregimiento registrado.")
            return redirect('lista_municipios')
        else:
            messages.error(request, "❌ No se pudo registrar. Verifique los datos ingresados.")
    else:
        form = MunicipioForm()

    return render(request, 'municipio/form.html', {
        'form': form,
        'titulo': 'Registrar Municipio/Corregimiento'
    })

@login_required
@permission_required('AppMunicipio.change_municipio', raise_exception=True)
def editar_municipio(request, pk):
    municipio = get_object_or_404(Municipio, pk=pk)

    if request.method == 'POST':
        form = MunicipioForm(request.POST, instance=municipio)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Municipio/Corregimiento actualizado.")
            return redirect('lista_municipios')
        else:
            messages.error(request, "❌ No se pudo actualizar. Revise la información ingresada.")
    else:
        form = MunicipioForm(instance=municipio)

    return render(request, 'municipio/form.html', {
        'form': form,
        'titulo': 'Editar Municipio/Corregimiento'
    })

@login_required
@permission_required('AppMunicipio.delete_municipio', raise_exception=True)
def eliminar_municipio(request, pk):
    municipio = get_object_or_404(Municipio, pk=pk)

    try:
        municipio.delete()
        messages.success(request, "✅ Municipio/Corregimiento eliminado.")
    except ProtectedError:
        messages.error(
            request,
            "❌ No se puede eliminar este municipio porque está asociado a votantes o puestos de votación."
        )

    return redirect('lista_municipios')

@login_required
def cambiar_estado_municipio(request, pk):
    municipio = get_object_or_404(Municipio, pk=pk)
    
    # Lógica para cambiar el estado
    if municipio.status == 'ACTIVE':
        municipio.status = 'INACTIVE'
        messages.warning(request, f"⚠️ Municipio/Corregimiento '{municipio.nombre}' marcado como INACTIVO.")
    else:
        municipio.status = 'ACTIVE'
        messages.success(request, f"✅ Municipio/Corregimiento '{municipio.nombre}' marcado como ACTIVO.")
    
    municipio.save()
    
    # Redirige a la página anterior (lista_municipios)
    return redirect(request.META.get('HTTP_REFERER', 'lista_municipios'))