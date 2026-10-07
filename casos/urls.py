from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_casos, name="lista_casos"), path("casos/", views.lista_casos, name="lista_casos"),
    path("casos/<int:pk>/", views.detalle_caso, name="detalle_caso"), path("casos/<int:pk>/pago/", views.registrar_pago, name="registrar_pago"),
    path("casos/<int:pk>/api/", views.api_caso, name="api_caso"), path("casos/api/<int:pk>/", views.api_caso, name="api_caso_alterna"),
    path("expedientes/<int:pk>/documento/", views.subir_documento, name="subir_documento"),
    path("clientes/", views.clientes_lista, name="clientes_lista"), path("clientes/nuevo/", views.cliente_nuevo, name="cliente_nuevo"),
    path("clientes/<int:pk>/editar/", views.cliente_editar, name="cliente_editar"), path("clientes/<int:pk>/eliminar/", views.cliente_eliminar, name="cliente_eliminar"),
]
