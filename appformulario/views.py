from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from django.http import HttpResponse
from django.contrib import messages
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from django.db.models import Q
from .forms import VotanteForm
from .models import votante
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
            Q(municipio_nacimiento__nombre__icontains=query) |
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
            messages.error(request, "❌ Hubo un error al registrar el votante. Verifique los datos.")
    else:
        form = VotanteForm()

    return render(request, 'votantes/form.html', {'form': form, 'titulo': 'Registrar Votante'})

from django.contrib import messages

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
            messages.error(request, "❌ No se pudo actualizar el votante. Revise la información ingresada.")
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



# -----------------------------------------------------------------------
# Función para exportar a Excel
def exportar_votantes_excel(request):
    # 1. Obtener datos (solo ACTIVOS)
    votantes = votante.objects.filter(status='ACTIVE').select_related(
        'puesto_votacion', 
        'puesto_votacion__municipio', 
        'municipio_nacimiento'
    )

    # 2. Construir datos
    data = []
    for v in votantes:
        # Lógica para campos vacíos del puesto
        nombre_puesto = ''
        municipio_puesto = ''
        direccion_puesto = ''
        
        if v.puesto_votacion:
            nombre_puesto = v.puesto_votacion.nombre_lugar
            direccion_puesto = v.puesto_votacion.direccion
            if v.puesto_votacion.municipio:
                municipio_puesto = str(v.puesto_votacion.municipio)

        data.append({
            'Nombres': v.nombre,
            'Apellidos': v.apellido,
            'Cédula': v.cedula,
            'Edad': v.edad,
            'Teléfono': v.telefono,
            'Líder': v.lider,
            'Municipio de Nacimiento': v.municipio_nacimiento.nombre if v.municipio_nacimiento else '',
            'Lugar de Votación': nombre_puesto,
            'Municipio del Puesto': municipio_puesto,
            'Dirección del Puesto': direccion_puesto,
            # 'Estado': v.get_status_display() # Retorna "Activo" o "Inactivo"
        })

    # 3. Crear DataFrame y escribir a memoria
    df = pd.DataFrame(data)
    buffer = BytesIO()
    
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Votantes')

    buffer.seek(0)
    wb = load_workbook(buffer)
    ws = wb.active

    # --- DEFINICIÓN DE ESTILOS ---
    
    # 1. Estilo para el Encabezado (Gris Oscuro con texto blanco)
    header_fill = PatternFill(start_color="404040", end_color="404040", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    
    # # 2. Estilos para el Estado 
    # # Verde Success (#198754)
    # success_fill = PatternFill(start_color="198754", end_color="198754", fill_type="solid")
    # # Gris Secondary (#6C757D)
    # secondary_fill = PatternFill(start_color="6C757D", end_color="6C757D", fill_type="solid")
    # # Texto Blanco para que contraste con el fondo de color
    # white_font = Font(color="FFFFFF")

    # --- APLICAR ESTILOS ---

    # 1. Aplicar estilo al encabezado y buscar índice de columna "Estado"
    ws.freeze_panes = 'A2' # Congelar encabezado
    estado_col_index = None

    for cell in ws[1]: # Recorrer primera fila
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center') # Centrar títulos
        
    #     # Detectar cuál columna es "Estado"
    #     if cell.value == "Estado":
    #         estado_col_index = cell.column # Guarda el número de columna (ej. 11)

    # # 2. Aplicar colores condicionales a la columna Estado
    # # Iteramos desde la fila 2 hasta el final
    # if estado_col_index:
    #     for row in range(2, ws.max_row + 1):
    #         cell = ws.cell(row=row, column=estado_col_index)
            
    #         # Verificamos el texto. Ajusta "Activo" según lo que devuelva get_status_display()
    #         if cell.value == "Activo": 
    #             cell.fill = success_fill
    #             cell.font = white_font
    #         else:
    #             cell.fill = secondary_fill
    #             cell.font = white_font
            
    #         # Centrar el texto del estado 
    #         cell.alignment = Alignment(horizontal='center')

    # 3. Ajustar ancho de columnas
    for column_cells in ws.columns:
        max_length = 0
        column = column_cells[0].column_letter
        for cell in column_cells:
            if cell.value:
                try:
                    max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
        ws.column_dimensions[column].width = max_length + 3

    # Guardar y Retornar
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=Listado_Votantes.xlsx'
    return response