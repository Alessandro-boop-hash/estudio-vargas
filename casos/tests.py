from datetime import date
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from .models import Caso, Cliente, EstadoCaso, Pago

class CasosTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nombres="Cliente Demo", documento="12345678", telefono="999999999", correo="demo@correo.pe")
        self.activo = EstadoCaso.objects.create(nombre="en proceso", permite_pagos=True)
        self.cerrado = EstadoCaso.objects.create(nombre="archivado", permite_pagos=False)
        self.caso = Caso.objects.create(codigo="C-1", titulo="Caso activo", descripcion="Demo", fecha_inicio=date.today(), cliente=self.cliente, estado=self.activo)
    def test_total_pagado_usa_agregacion(self):
        Pago.objects.create(caso=self.caso, monto=Decimal("10.25"), fecha=date.today(), descripcion="A")
        Pago.objects.create(caso=self.caso, monto=Decimal("20.75"), fecha=date.today(), descripcion="B")
        self.assertEqual(self.caso.total_pagado(), Decimal("31.00"))
    def test_pago_no_permitido_es_validado_en_modelo(self):
        self.caso.estado = self.cerrado; self.caso.save()
        with self.assertRaises(ValidationError): Pago(caso=self.caso, monto=10, fecha=date.today(), descripcion="No válido").full_clean()
    def test_pago_por_post_actualiza_total(self):
        self.client.post(reverse("registrar_pago", args=[self.caso.id]), {"monto": "100.00", "descripcion": "Portal"})
        self.assertEqual(self.caso.total_pagado(), Decimal("100.00"))
    def test_api_y_cookie_de_estado(self):
        response = self.client.get(reverse("lista_casos"), {"estado": self.activo.id})
        self.assertIn("ultimo_estado", response.cookies)
        data = self.client.get(reverse("api_caso", args=[self.caso.id])).json()
        self.assertEqual(data["codigo"], "C-1")
