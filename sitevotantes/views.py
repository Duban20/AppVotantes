from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from appformulario.models import LiderEG, SubLider, Votante


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
    Calcula y muestra los KPIs de toda la base de datos, 
    sin filtrar por estado para ver el conteo total.
    """
    
    # 1. Conteos por Rol (Todos los registros)
    # Filtramos directamente sobre el modelo Votante según el campo 'rol'
    total_votantes = Votante.objects.filter(rol='VOTANTE').count()
    
    # Si tus modelos de Líder y Sublíder son extensiones o perfiles:
    total_lideres = LiderEG.objects.count()
    total_sublideres = SubLider.objects.count()
    
    # Si los cuentas directamente desde la tabla Votante por su rol:
    # total_lideres = Votante.objects.filter(rol='LIDER_VOTANTE').count()
    # total_sublideres = Votante.objects.filter(rol='SUBLIDER').count()

    # 2. Cálculo del Total General (Suma de toda la estructura)
    total_general = Votante.objects.count()

    # 3. Lógica para evitar división por cero en gráficos futuros
    total_para_calculos = total_general if total_general > 0 else 1 

    context = {
        'total_votantes': total_votantes,
        'total_lideres': total_lideres,
        'total_sublideres': total_sublideres,
        'total_general': total_general,
        'total_para_calculos': total_para_calculos,
        # Aquí puedes añadir más datos como:
        # 'top_lideres': LiderEG.objects.annotate(num_votantes=Count('votante')).order_by('-num_votantes')[:5],
    }

    return render(request, 'dashboard.html', context)