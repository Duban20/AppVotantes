from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from django.http import HttpResponse
from django.contrib import messages
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from django.db.models import Q

from applider.models import Lider
from .forms import VotanteForm
from .models import votante
from django.http import JsonResponse
from appmesa.models import Mesa
from io import BytesIO
import pandas as pd


@login_required
@permission_required('appformulario.view_votante', raise_exception=True)
def lista_votantes(request):
    query = request.GET.get('q')
    
    status_filter = request.GET.get('status')
    
    votantes = votante.objects.all()

    # Aplicar el filtro de estado si existe y no está vacío
    if status_filter:
        votantes = votantes.filter(status=status_filter)
    
    # Aplicar el filtro de búsqueda general (q)
    if query:
        votantes = votantes.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(cedula__icontains=query) |
            Q(puesto_votacion__nombre_lugar__icontains=query)
        )
    
    # Pasar el estado activo al template para resaltar el botón
    return render(request, 'votantes/lista.html', {
        'votantes': votantes,
        'query': query,
        'status_filter': status_filter 
    })

@login_required
@permission_required('appformulario.add_votante', raise_exception=True)
def crear_votante(request):
    if request.method == 'POST':
        form = VotanteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ El votante fue registrado exitosamente.")
            return redirect('lista_votantes')
    else:
        form = VotanteForm()

    return render(request, 'votantes/form.html', {'form': form, 'titulo': 'Registrar Votante'})


@login_required
@permission_required('appformulario.change_votante', raise_exception=True)
def editar_votante(request, pk):
    vot = get_object_or_404(votante, pk=pk)
    if request.method == 'POST':
        form = VotanteForm(request.POST, instance=vot)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Los datos del votante fueron actualizados correctamente.")
            return redirect('lista_votantes')
    else:
        form = VotanteForm(instance=vot)

    return render(request, 'votantes/form.html', {'form': form, 'titulo': 'Editar Votante'})


@login_required
@permission_required('appformulario.delete_votante', raise_exception=True)
def eliminar_votante(request, pk):
    vot = get_object_or_404(votante, pk=pk)
    try:
        vot.delete()
        messages.success(request, "✅ Votante eliminado.")
    except ProtectedError:
        messages.error(request, "❌ No se puede eliminar este votante.")
    return redirect('lista_votantes')

@login_required
@permission_required('appformulario.change_status_votante', raise_exception=True)
def cambiar_estado_votante(request, pk):
    vot = get_object_or_404(votante, pk=pk)
    
    if vot.status == 'ACTIVE':
        vot.status = 'INACTIVE'
        messages.warning(request, f"⚠️ Votante {vot.nombre} {vot.apellido} marcado como INACTIVO.")
    else:
        vot.status = 'ACTIVE'
        messages.success(request, f"✅ Votante {vot.nombre} {vot.apellido} marcado como ACTIVO.")
    
    vot.save()
    
    # Redirige a la página de lista, conservando los filtros si es posible
    return redirect(request.META.get('HTTP_REFERER', 'lista_votantes'))

@login_required
def obtener_mesas_por_puesto(request):
    puesto_id = request.GET.get("puesto_id")
    mesas = Mesa.objects.filter(puesto_votacion_id=puesto_id, status="ACTIVE")

    data = [
        {"id": m.id, "numero": m.numero}
        for m in mesas
    ]
    return JsonResponse({"mesas": data})

@login_required
def ajax_nuevo_lider(request):
    if request.method == "POST":

        nombre = request.POST.get("nombre")
        cedula = request.POST.get("cedula")
        telefono = request.POST.get("telefono")

        lider = Lider.objects.create(
            nombre=nombre,
            cedula=cedula,
            telefono=telefono
        )

        return JsonResponse({
            "id": lider.id,
            "nombre": lider.nombre,
            "cedula": lider.cedula,
            "telefono": lider.telefono
        })

    return JsonResponse({"error": "Método no permitido"}, status=400)




# -----------------------------------------------------------------------
# Función para exportar a Excel
@login_required
def exportar_votantes_excel(request):

    # Obtener solo votantes activos
    votantes = votante.objects.filter(status='ACTIVE').select_related(
        'mesa',
        'mesa__puesto_votacion',
        'mesa__puesto_votacion__municipio',
        'lider'
    )

    data = []
    for v in votantes:

        # Datos del puesto de votación
        puesto = v.mesa.puesto_votacion if v.mesa else None

        nombre_puesto = puesto.nombre_lugar if puesto else ''
        direccion_puesto = puesto.direccion if puesto else ''
        municipio_puesto = puesto.municipio.nombre if puesto and puesto.municipio else ''
        departamento_puesto = (
            puesto.municipio.departamento.nombre
            if puesto and puesto.municipio and puesto.municipio.departamento
            else ''
        )

        data.append({
            'Nombres': v.nombre,
            'Apellidos': v.apellido,
            'Cédula': v.cedula,
            'Dirección de residencia': v.direccion_residencia,
            'Barrio de residencia': v.barrio_residencia,
            'Teléfono': v.telefono,
            'Líder': v.lider.nombre if v.lider else '',
            'Documento líder': v.lider.cedula,
            'Teléfono líder': v.lider.telefono,
            'Lugar de Votación': nombre_puesto,
            'Mesa': v.mesa.numero,
            'Dirección': direccion_puesto,
            'Municipio': municipio_puesto,
            'Departamento': departamento_puesto,
        })

    # Crear DataFrame
    df = pd.DataFrame(data)
    buffer = BytesIO()

    # Escribir Excel inicial
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Votantes')

    buffer.seek(0)
    wb = load_workbook(buffer)
    ws = wb.active

    # Estilos
    header_fill = PatternFill(start_color="404040", end_color="404040", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    ws.freeze_panes = 'A2'

    ws = wb.active

    # -----------------------------------------
    # ESTILOS
    # -----------------------------------------
    header_fill = PatternFill(start_color="404040", end_color="404040", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)

    zebra_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Congelar encabezado
    ws.freeze_panes = 'A2'

    # -----------------------------------------
    # ESTILAR ENCABEZADO
    # -----------------------------------------
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', wrap_text=True)
        cell.border = thin_border

    # Activar auto-filtros
    ws.auto_filter.ref = ws.dimensions

    # -----------------------------------------
    # ZEBRA + BORDES + WRAP TEXT
    # -----------------------------------------
    for row_idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        # Zebra: filas pares = gris suave
        if row_idx % 2 == 0:
            for cell in row:
                cell.fill = zebra_fill

        # Bordes y ajuste de texto para todas las celdas
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(wrap_text=True, vertical='top')

    # -----------------------------------------
    # AUTO-ANCHO DE COLUMNAS (con límite)
    # -----------------------------------------
    for col in ws.columns:
        max_len = 0
        col_letter = col[0].column_letter

        for cell in col:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))

        # Evita columnas gigantes (máximo 40 caracteres de ancho)
        max_len = min(max_len, 40)

        ws.column_dimensions[col_letter].width = max_len + 3


    # Exportar archivo
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=Listado_Votantes.xlsx'

    return response