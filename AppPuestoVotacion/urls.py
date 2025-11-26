from django.urls import path
from .views import cambiar_estado_puesto, lista_puestos, crear_puesto, editar_puesto, eliminar_puesto

urlpatterns = [
    path('', lista_puestos, name='lista_puestos'),
    path('crear/', crear_puesto, name='crear_puesto'),
    path('editar/<int:pk>/', editar_puesto, name='editar_puesto'),
    path('eliminar/<int:pk>/', eliminar_puesto, name='eliminar_puesto'),
    path('estado/<int:pk>/', cambiar_estado_puesto, name='cambiar_estado_puesto'),
]
