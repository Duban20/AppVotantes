from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from appformulario.models import Votante


def home(request):
    """Muestra la Landing Page (home.html) si no está logueado."""
    # solo redirige al dashboard si el usuario está logueado, 
    # o muestra la landing page si no lo está.
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'home.html')


# Vista para el Dashboard
@login_required 
def dashboard(request):
    """
    Calcula y muestra los KPIs. Esta vista solo es accesible si el usuario
    está autenticado gracias a @login_required.
    """
    
    votantes_activos = Votante.objects.filter(status='ACTIVE')

    # --- CÁLCULO DE KPIs (Toda tu lógica va aquí) ---
    total_votantes = votantes_activos.filter(rol='VOTANTE').count()
    total_lideres = votantes_activos.filter(rol='LIDER_VOTANTE').count()
    
    # ... (Añade el cálculo de Top 5 Líderes y Votantes por Departamento aquí) ...
    # Ejemplo:
    # top_lideres = Votante.objects.filter(...) 
    # votantes_por_departamento = Departamento.objects.annotate(...) 

    total_votantes_general = total_votantes if total_votantes > 0 else 1 
    
    context = {
        'total_votantes': total_votantes,
        'total_lideres': total_lideres,
        # ... (Añade el resto del contexto) ...
        'total_votantes_general': total_votantes_general,
    }

    return render(request, 'dashboard.html', context)