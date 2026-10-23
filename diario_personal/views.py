from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import viewsets
from . import serializer as ser

from .models import (
	Adjunto,
	Categoria,
	Comentario,
	Entrada,
	HistorialEstado,
	PerfilAcceso,
	SesionActividad,
	Usuario,
)

from .serializer import (
	AdjuntoSerializer,
	CategoriaSerializer,
	ComentarioSerializer,
	EntradaSerializer,
	HistorialEstadoSerializer,
	PerfilAccesoSerializer,
	SesionActividadSerializer,
	UsuarioSerializer,
)

# Genera vistas basadas en conjuntos de datos para cada modelo definido en models.py. Cada vista utiliza un serializador correspondiente para convertir los datos del modelo a un formato adecuado para la API RESTful.
class AdjuntoViewSet(viewsets.ModelViewSet):
	queryset = Adjunto.objects.all()
	serializer_class = AdjuntoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
	queryset = Categoria.objects.all()
	serializer_class = CategoriaSerializer

class ComentarioViewSet(viewsets.ModelViewSet):
	queryset = Comentario.objects.all()
	serializer_class = ComentarioSerializer

class EntradaViewSet(viewsets.ModelViewSet):
	queryset = Entrada.objects.all()
	serializer_class = EntradaSerializer

class HistorialEstadoViewSet(viewsets.ModelViewSet):
	queryset = HistorialEstado.objects.all()
	serializer_class = HistorialEstadoSerializer

class PerfilAccesoViewSet(viewsets.ModelViewSet):
	queryset = PerfilAcceso.objects.all()
	serializer_class = PerfilAccesoSerializer

class SesionActividadViewSet(viewsets.ModelViewSet):
	queryset = SesionActividad.objects.all()
	serializer_class = SesionActividadSerializer

#class UsuarioViewSet(viewsets.ModelViewSet):
#	queryset = Usuario.objects.all()
#	serializer_class = UsuarioSerializer

#class UsuarioViewSet(viewsets.ModelViewSet):
#	serializer_class = UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
	queryset = Usuario.objects.all()
	serializer_class = ser.UsuarioSerializer

class UserListView(ListView):
	model = Usuario
	template_name = 'diario_personal/user_list.html'
	context_object_name = 'users'

# Main
def home(request):
	return render(request, 'diario_personal/home.html')

def not_found(request, exception):
	return render(request, 'diario_personal/not_found.html', status=404)

