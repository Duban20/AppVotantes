from django.urls import path
from .views import cambiar_estado_municipio, lista_municipios, crear_municipio, editar_municipio, eliminar_municipio

urlpatterns = [
    path('', lista_municipios, name='lista_municipios'),
    path('crear/', crear_municipio, name='crear_municipio'),
    path('editar/<int:pk>/', editar_municipio, name='editar_municipio'),
    path('eliminar/<int:pk>/', eliminar_municipio, name='eliminar_municipio'),
    path('estado/<int:pk>/', cambiar_estado_municipio, name='cambiar_estado_municipio'),
]