from django.contrib import admin
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

# Register your models here.
admin.site.site_header = "Diario Personal"
admin.site.register(
	[
		Adjunto,
		Categoria,
		Comentario,
		Entrada,
		HistorialEstado,
		PerfilAcceso,
		SesionActividad,
		Usuario,
	]
)