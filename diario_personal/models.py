"""
Modelos Django para el sistema "Diario Personal".

Entidades: Usuario, PerfilAcceso, Categoria, Entrada, HistorialEstado,
Adjunto, Comentario, SesionActividad.

Requiere: pip install django --break-system-packages
Configurar AUTH_USER_MODEL = 'diario.Usuario' en settings.py
"""

from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.db import models


# ---------------------------------------------------------------------------
# Usuario y perfiles de acceso
# ---------------------------------------------------------------------------

class PerfilAcceso(models.Model):
    """Rol/perfil que determina permisos dentro del sistema."""

    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    puede_administrar = models.BooleanField(default=False)
    puede_auditar = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Perfil de acceso"
        verbose_name_plural = "Perfiles de acceso"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    """Usuario del sistema. Extiende el modelo de auth de Django."""

    perfiles = models.ManyToManyField(
        PerfilAcceso, related_name="usuarios", blank=True
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    # Se sobreescriben para evitar el choque de reverse accessors con
    # auth.User (fields.E304) al usar un modelo de usuario personalizado.
    groups = models.ManyToManyField(
        Group,
        related_name="diario_usuarios",
        blank=True,
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="diario_usuarios_permisos",
        blank=True,
        verbose_name="user permissions",
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username

    def tiene_perfil(self, nombre_perfil):
        return self.perfiles.filter(nombre=nombre_perfil).exists()


# ---------------------------------------------------------------------------
# Categorización
# ---------------------------------------------------------------------------

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


# ---------------------------------------------------------------------------
# Entrada (núcleo del dominio)
# ---------------------------------------------------------------------------

class Entrada(models.Model):

    class Estado(models.TextChoices):
        BORRADOR = "borrador", "Borrador"
        PUBLICADA = "publicada", "Publicada"
        ARCHIVADA = "archivada", "Archivada"
        ELIMINADA = "eliminada", "Eliminada"

    class Visibilidad(models.TextChoices):
        PUBLICA = "publica", "Pública"
        PRIVADA = "privada", "Privada"

    # Transiciones de estado permitidas (regla de negocio / integridad)
    TRANSICIONES_VALIDAS = {
        Estado.BORRADOR: {Estado.PUBLICADA, Estado.ELIMINADA},
        Estado.PUBLICADA: {Estado.ARCHIVADA, Estado.ELIMINADA},
        Estado.ARCHIVADA: {Estado.PUBLICADA, Estado.ELIMINADA},
        Estado.ELIMINADA: set(),  # estado terminal
    }

    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="entradas"
    )
    categorias = models.ManyToManyField(
        Categoria, related_name="entradas", blank=True
    )
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.BORRADOR, db_index=True
    )
    visibilidad = models.CharField(
        max_length=10,
        choices=Visibilidad.choices,
        default=Visibilidad.PRIVADA,
        db_index=True,
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_index=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"
        ordering = ["-fecha_creacion"]
        indexes = [
            models.Index(fields=["autor", "estado"]),
            models.Index(fields=["visibilidad", "estado"]),
        ]

    def __str__(self):
        return f"{self.titulo} ({self.get_estado_display()})"

    def clean(self):
        # Regla de integridad: solo entradas eliminadas por borrado lógico
        if self.pk:
            estado_actual = Entrada.objects.get(pk=self.pk).estado
            if (
                estado_actual != self.estado
                and self.estado not in self.TRANSICIONES_VALIDAS.get(estado_actual, set())
            ):
                raise ValidationError(
                    f"Transición inválida: {estado_actual} -> {self.estado}"
                )

    def cambiar_estado(self, nuevo_estado, usuario, motivo=""):
        """Cambia el estado validando la transición y registra el historial (auditoría)."""
        estado_anterior = self.estado
        if nuevo_estado not in self.TRANSICIONES_VALIDAS.get(estado_anterior, set()):
            raise ValidationError(
                f"Transición inválida: {estado_anterior} -> {nuevo_estado}"
            )
        self.estado = nuevo_estado
        self.save(update_fields=["estado", "fecha_modificacion"])
        HistorialEstado.objects.create(
            entrada=self,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            usuario=usuario,
            motivo=motivo,
        )


# ---------------------------------------------------------------------------
# Auditoría de cambios de estado
# ---------------------------------------------------------------------------

class HistorialEstado(models.Model):
    """Registro histórico e inmutable de cada cambio de estado de una Entrada."""

    entrada = models.ForeignKey(
        Entrada, on_delete=models.CASCADE, related_name="historial_estados"
    )
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, related_name="cambios_realizados"
    )
    fecha = models.DateTimeField(auto_now_add=True, db_index=True)
    motivo = models.TextField(blank=True)

    class Meta:
        verbose_name = "Historial de estado"
        verbose_name_plural = "Historial de estados"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.entrada_id}: {self.estado_anterior} -> {self.estado_nuevo}"

    def save(self, *args, **kwargs):
        # Inmutable: no se permite editar un registro de auditoría ya creado
        if self.pk:
            raise ValidationError("El historial de estado no puede modificarse.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("El historial de estado no puede eliminarse.")


# ---------------------------------------------------------------------------
# Recursos multimedia
# ---------------------------------------------------------------------------

class Adjunto(models.Model):

    class Tipo(models.TextChoices):
        IMAGEN = "imagen", "Imagen"
        AUDIO = "audio", "Audio"
        VIDEO = "video", "Video"
        DOCUMENTO = "documento", "Documento"

    entrada = models.ForeignKey(
        Entrada, on_delete=models.CASCADE, related_name="adjuntos"
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    archivo = models.FileField(upload_to="adjuntos/%Y/%m/")
    tamano_bytes = models.PositiveIntegerField(null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Adjunto"
        verbose_name_plural = "Adjuntos"
        ordering = ["-fecha_subida"]

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.entrada_id}"


# ---------------------------------------------------------------------------
# Interacción entre usuarios
# ---------------------------------------------------------------------------

class Comentario(models.Model):
    entrada = models.ForeignKey(
        Entrada, on_delete=models.CASCADE, related_name="comentarios"
    )
    autor = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="comentarios"
    )
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ["fecha"]

    def __str__(self):
        return f"Comentario de {self.autor} en {self.entrada_id}"

    def clean(self):
        # Regla de negocio: no se puede comentar una entrada eliminada
        if self.entrada.estado == Entrada.Estado.ELIMINADA:
            raise ValidationError("No se puede comentar una entrada eliminada.")


# ---------------------------------------------------------------------------
# Actividad / indicadores de gestión
# ---------------------------------------------------------------------------

class SesionActividad(models.Model):
    """Bitácora de actividad del usuario, base para indicadores de uso."""

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="sesiones"
    )
    accion = models.CharField(max_length=100)  # login, logout, crear_entrada, etc.
    fecha = models.DateTimeField(auto_now_add=True, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    detalle = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Sesión / actividad"
        verbose_name_plural = "Sesiones / actividad"
        ordering = ["-fecha"]
        indexes = [
            models.Index(fields=["usuario", "fecha"]),
        ]

    def __str__(self):
        return f"{self.usuario} - {self.accion} ({self.fecha:%Y-%m-%d %H:%M})"