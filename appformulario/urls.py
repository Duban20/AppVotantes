from django.urls import path
from .views import (
    cambiar_estado_votante,
    lista_votantes,
    crear_votante,
    editar_votante,
    eliminar_votante
)
from . import views

urlpatterns = [
    path('', lista_votantes, name='lista_votantes'),
    path('crear/', crear_votante, name='crear_votante'),
    path('editar/<int:pk>/', editar_votante, name='editar_votante'),
    path('eliminar/<int:pk>/', eliminar_votante, name='eliminar_votante'),
    path('estado/<int:pk>/', cambiar_estado_votante, name='cambiar_estado_votante'),
    path('exportar/', views.exportar_votantes_excel, name='exportar_votantes'),
]
