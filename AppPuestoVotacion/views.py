from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from .forms import PuestoVotacionForm
from django.contrib import messages
from .models import PuestoVotacion
from django.db.models import Q

@login_required
@permission_required('AppPuestoVotacion.view_puestovotacion', raise_exception=True)
def lista_puestos(request):
    # 1. Capturar filtros
    query = request.GET.get('q')
    status_filter = request.GET.get('status')
    
    puestos = PuestoVotacion.objects.all()

    # 2. Aplicar filtro de estado
    if status_filter:
        puestos = puestos.filter(status=status_filter)
        
    # 3. Aplicar filtro de búsqueda general
    if query:
        puestos = puestos.filter(
            Q(nombre_lugar__icontains=query) |
            Q(direccion__icontains=query) |
            Q(municipio__nombre__icontains=query)
        )
        
    return render(request, 'puesto_votacion/lista.html', {
        'puestos': puestos,
        'query': query, # Pasar el query al template
        'status_filter': status_filter # Pasar el filtro de estado al template
    })

@login_required
@permission_required('AppPuestoVotacion.add_puestovotacion', raise_exception=True)
def crear_puesto(request):
    if request.method == 'POST':
        form = PuestoVotacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Puesto de votación registrado.")
            return redirect('lista_puestos')
        else:
            messages.error(request, "❌ No se pudo registrar. Verifique los datos ingresados.")
    else:
        form = PuestoVotacionForm()

    return render(request, 'puesto_votacion/form.html', {
        'form': form,
        'titulo': 'Registrar Puesto de Votación'
    })

@login_required
@permission_required('AppPuestoVotacion.change_puestovotacion', raise_exception=True)
def editar_puesto(request, pk):
    puesto = get_object_or_404(PuestoVotacion, pk=pk)

    if request.method == 'POST':
        form = PuestoVotacionForm(request.POST, instance=puesto)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Puesto de votación actualizado.")
            return redirect('lista_puestos')
        else:
            messages.error(request, "❌ No se pudo actualizar. Revise la información ingresada.")
    else:
        form = PuestoVotacionForm(instance=puesto)

    return render(request, 'puesto_votacion/form.html', {
        'form': form,
        'titulo': 'Editar Puesto de Votación'
    })

@login_required
@permission_required('AppPuestoVotacion.delete_puestovotacion', raise_exception=True)
def eliminar_puesto(request, pk):
    puesto = get_object_or_404(PuestoVotacion, pk=pk)

    try:
        puesto.delete()
        messages.success(request, "✅ Puesto de votación eliminado.")
    except ProtectedError:
        messages.error(
            request,
            "❌ No se puede eliminar este puesto porque está asociado a uno o más votantes."
        )

    return redirect('lista_puestos')

@login_required
def cambiar_estado_puesto(request, pk):
    puesto = get_object_or_404(PuestoVotacion, pk=pk)
    
    if puesto.status == 'ACTIVE':
        puesto.status = 'INACTIVE'
        messages.warning(request, f"⚠️ Puesto de votación '{puesto.nombre_lugar}' marcado como INACTIVO.")
    else:
        puesto.status = 'ACTIVE'
        messages.success(request, f"✅ Puesto de votación '{puesto.nombre_lugar}' marcado como ACTIVO.")
    
    puesto.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'lista_puestos'))