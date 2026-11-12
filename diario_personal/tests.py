from django.test import SimpleTestCase

from django.urls import resolve, reverse

from .views import ComentarioUpdateView


class ComentarioUpdateViewTests(SimpleTestCase):
    def test_edit_comentario_route_uses_update_view(self):
        match = resolve(reverse("edit_comentario", kwargs={"pk": 1}))

        self.assertIs(match.func.view_class, ComentarioUpdateView)
