from django.urls import path, include
from rest_framework import routers
from diario_personal import views

enrutador = routers.DefaultRouter()

enrutador.register(r'adjuntos', views.AdjuntoViewSet)
enrutador.register(r'categorias', views.CategoriaViewSet)
enrutador.register(r'comentarios', views.ComentarioViewSet)
enrutador.register(r'entradas', views.EntradaViewSet)
enrutador.register(r'historiales-estado', views.HistorialEstadoViewSet)
enrutador.register(r'perfiles-acceso', views.PerfilAccesoViewSet)
enrutador.register(r'sesiones-actividad', views.SesionActividadViewSet)
enrutador.register(r'usuarios', views.UsuarioViewSet)


urlpatterns = [
    path('', include(enrutador.urls)),
    path('usuarios/', views.UserListView.as_view(), name='listado_usuarios'),
]