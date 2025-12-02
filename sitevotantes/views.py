from django.shortcuts import redirect, render


def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin/')
        else:
            return redirect('personas/')  # ruta del trabajador
        
    return render(request, 'home.html')