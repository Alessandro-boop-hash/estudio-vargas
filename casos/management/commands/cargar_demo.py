from datetime import date
from decimal import Decimal
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from casos.models import Caso, Cliente, EstadoCaso, Expediente, Pago, PerfilAbogado

class Command(BaseCommand):
    help = "Carga datos demostrativos de la evaluación"
    def handle(self, *args, **kwargs):
        estados = {}
        for nombre, permite in [("iniciado", True), ("en proceso", True), ("cancelado", False), ("terminado", False), ("archivado", False)]:
            estados[nombre], _ = EstadoCaso.objects.get_or_create(nombre=nombre, defaults={"permite_pagos": permite})
            estados[nombre].permite_pagos = permite; estados[nombre].save()
        grupo, _ = Group.objects.get_or_create(name="Abogados")
        abogados = []
        for username, first, last, coleg, esp in [("mgarcia", "María", "García", "CAL-1001", "Civil"), ("jtorres", "José", "Torres", "CAL-1002", "Laboral")]:
            user, created = User.objects.get_or_create(username=username, defaults={"first_name": first, "last_name": last, "email": f"{username}@vargas.pe"})
            if created: user.set_password("Abogado2026!"); user.save()
            user.groups.add(grupo); PerfilAbogado.objects.get_or_create(usuario=user, defaults={"numero_colegiatura": coleg, "especialidad": esp}); abogados.append(user)
        admin, created = User.objects.get_or_create(username="admin", defaults={"is_staff": True, "is_superuser": True, "email": "admin@vargas.pe"})
        admin.is_staff = admin.is_superuser = True; admin.set_password("Admin2026!"); admin.save()
        cliente, _ = Cliente.objects.get_or_create(documento="20123456789", defaults={"nombres": "Empresa Andina SAC", "telefono": "(01) 555-0101", "correo": "contacto@andina.pe"})
        caso1, _ = Caso.objects.get_or_create(codigo="CAS-2026-001", defaults={"titulo": "Cobranza comercial", "descripcion": "Proceso de cobranza por obligaciones comerciales.", "fecha_inicio": date(2026, 3, 1), "cliente": cliente, "estado": estados["en proceso"]})
        caso1.abogados.set(abogados)
        caso2, _ = Caso.objects.get_or_create(codigo="CAS-2026-002", defaults={"titulo": "Revisión contractual", "descripcion": "Revisión y archivo de contrato comercial.", "fecha_inicio": date(2026, 4, 10), "cliente": cliente, "estado": estados["archivado"]})
        Expediente.objects.get_or_create(numero="EXP-2026-001", defaults={"juzgado": "Primer Juzgado Civil de Lima", "fecha_presentacion": date(2026, 3, 5), "caso": caso1})
        Expediente.objects.get_or_create(numero="EXP-2026-002", defaults={"juzgado": "Segundo Juzgado Civil de Lima", "fecha_presentacion": date(2026, 3, 8), "caso": caso1})
        for monto, fecha, descripcion in [("1500.00", date(2026, 3, 10), "Adelanto de honorarios"), ("850.50", date(2026, 3, 20), "Gastos procesales"), ("1200.00", date(2026, 4, 1), "Segundo pago de honorarios")]:
            Pago.objects.get_or_create(caso=caso1, monto=Decimal(monto), fecha=fecha, defaults={"descripcion": descripcion})
        self.stdout.write(self.style.SUCCESS(f"Cliente: {cliente}; casos: {cliente.casos.count()}; abogados de {caso1.codigo}: {caso1.abogados.count()}; expedientes: {caso1.expedientes.count()}; total: S/ {caso1.total_pagado():.2f}"))
