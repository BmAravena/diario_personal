from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Categoria, Comentario, Usuario


class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nombre de usuario"
        self.fields["email"].label = "Correo electrónico"
        self.fields["first_name"].label = "Nombre"
        self.fields["last_name"].label = "Apellido"
        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Confirmar contraseña"

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ("username", "email", "first_name", "last_name")
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico",
            "first_name": "Nombre",
            "last_name": "Apellido",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class CategoriaCreationForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ("nombre", "descripcion")
        labels = {
            "nombre": "Nombre",
            "descripcion": "Descripción",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class ComentarioCreationForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ("entrada", "autor", "contenido")
        labels = {
            "entrada": "Entrada",
            "autor": "Autor",
            "contenido": "Comentario",
        }
        widgets = {
            "entrada": forms.Select(attrs={"class": "form-select"}),
            "autor": forms.Select(attrs={"class": "form-select"}),
            "contenido": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
