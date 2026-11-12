from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from rest_framework import viewsets
from . import serializer as ser
from .forms import (
	CategoriaCreationForm,
	CategoriaUpdateForm,
	ComentarioCreationForm,
	ComentarioUpdateForm,
	UsuarioCreationForm,
	UsuarioUpdateForm,
)

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

# LIST VIEWS
class UserListView(ListView):
	model = Usuario
	template_name = 'diario_personal/usersViews/user_list.html'
	context_object_name = 'users'

class CategoriaListView(ListView):
	model = Categoria
	template_name = 'diario_personal/categoriasViews/categoria_list.html'
	context_object_name = 'categorias'


# CREATE VIEWS
class UserCreateView(CreateView):
	model = Usuario
	form_class = UsuarioCreationForm
	template_name = 'diario_personal/usersViews/create_user.html'
	success_url = reverse_lazy('listado_usuarios')


# UPDATE VIEWS
class UserUpdateView(UpdateView):
	model = Usuario
	form_class = UsuarioUpdateForm
	template_name = 'diario_personal/usersViews/edit_usuario.html'
	success_url = reverse_lazy('listado_usuarios')


class CategoriaUpdateView(UpdateView):
	model = Categoria
	form_class = CategoriaUpdateForm
	template_name = 'diario_personal/categoriasViews/edit_categoria.html'
	success_url = reverse_lazy('listado_categorias')


class ComentarioListView(ListView):
	model = Comentario
	template_name = 'diario_personal/comentariosViews/comentarios_list.html'
	context_object_name = 'comentarios'

class ComentarioCreateView(CreateView):
	model = Comentario
	form_class = ComentarioCreationForm
	template_name = 'diario_personal/comentariosViews/create_comentario.html'
	success_url = reverse_lazy('listado_comentarios')

class ComentarioUpdateView(UpdateView):
	model = Comentario
	form_class = ComentarioUpdateForm
	template_name = 'diario_personal/comentariosViews/edit_comentarios.html'
	success_url = reverse_lazy('listado_comentarios')

class CategoriaCreateView(CreateView):
	model = Categoria
	form_class = CategoriaCreationForm
	template_name = 'diario_personal/categoriasViews/create_categoria.html'
	success_url = reverse_lazy('listado_categorias')


# Main
def home(request):
	return render(request, 'diario_personal/home.html')

def not_found(request, exception):
	return render(request, 'diario_personal/not_found.html', status=404)
