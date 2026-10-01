from rest_framework import serializers

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

class AdjuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adjunto
        #fields = '__all__' # Get all fields from the model
        fields = ['nombre', 'tipo', 'ruta', 'entrada'] # Get specific fields from the model

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'

class EntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrada
        fields = '__all__'

class HistorialEstadoSerializer(serializers.ModelSerializer):   
    class Meta:
        model = HistorialEstado
        fields = '__all__'        

class PerfilAccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilAcceso
        fields = '__all__'

class SesionActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SesionActividad
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'