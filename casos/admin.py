from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Caso, Cliente, EstadoCaso, Expediente, Pago, PerfilAbogado

class PerfilAbogadoInline(admin.StackedInline):
    model = PerfilAbogado
    extra = 0

class UsuarioAdmin(UserAdmin):
    inlines = [PerfilAbogadoInline]

class ExpedienteInline(admin.TabularInline):
    model = Expediente
    extra = 1

class PagoInline(admin.TabularInline):
    model = Pago
    extra = 1

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombres", "documento", "telefono", "correo")
    search_fields = ("nombres", "documento", "correo")

@admin.register(EstadoCaso)
class EstadoCasoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "permite_pagos")
    search_fields = ("nombre",)
    list_filter = ("permite_pagos",)

@admin.register(Caso)
class CasoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "titulo", "cliente", "estado", "total_pagado", "fecha_inicio")
    search_fields = ("codigo", "titulo", "cliente__nombres")
    list_filter = ("estado", "fecha_inicio")
    filter_horizontal = ("abogados",)
    inlines = [ExpedienteInline, PagoInline]

@admin.register(Expediente)
class ExpedienteAdmin(admin.ModelAdmin):
    list_display = ("numero", "juzgado", "caso", "fecha_presentacion", "documento")
    search_fields = ("numero", "juzgado", "caso__codigo")
    list_filter = ("juzgado", "fecha_presentacion")

admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)
admin.site.site_header = "Vargas & Asociados - Gestión de Casos"
admin.site.site_title = "Gestión de Casos"
admin.site.index_title = "Administración del estudio jurídico"
