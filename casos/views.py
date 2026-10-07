from datetime import date
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ClienteForm, DocumentoExpedienteForm
from .models import Caso, Cliente, EstadoCaso, Pago, Expediente

def clientes_lista(request):
    return render(request, "casos/clientes_lista.html", {"clientes": Cliente.objects.all()})

def cliente_nuevo(request):
    form = ClienteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Cliente creado correctamente."); return redirect("clientes_lista")
    return render(request, "casos/cliente_form.html", {"form": form, "titulo": "Nuevo cliente"})

def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk); form = ClienteForm(request.POST or None, instance=cliente)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Cliente actualizado correctamente."); return redirect("clientes_lista")
    return render(request, "casos/cliente_form.html", {"form": form, "titulo": "Editar cliente"})

def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        try: cliente.delete(); messages.success(request, "Cliente eliminado correctamente.")
        except Exception: messages.error(request, "No se puede eliminar un cliente con casos registrados.")
        return redirect("clientes_lista")
    return render(request, "casos/cliente_confirmar_eliminar.html", {"cliente": cliente})

def lista_casos(request):
    estado_id = request.GET.get("estado") or request.COOKIES.get("ultimo_estado")
    casos = Caso.objects.select_related("cliente", "estado").prefetch_related("abogados")
    if estado_id: casos = casos.filter(estado_id=estado_id)
    response = render(request, "casos/lista_casos.html", {"casos": casos, "estados": EstadoCaso.objects.all(), "estado_actual": str(estado_id or "")})
    if request.GET.get("estado") is not None: response.set_cookie("ultimo_estado", request.GET.get("estado", ""), max_age=60 * 60 * 24 * 30)
    return response

def detalle_caso(request, pk):
    caso = get_object_or_404(Caso.objects.select_related("cliente", "estado").prefetch_related("abogados", "expedientes", "pagos"), pk=pk)
    return render(request, "casos/detalle_caso.html", {"caso": caso, "documento_form": DocumentoExpedienteForm()})

def registrar_pago(request, pk):
    caso = get_object_or_404(Caso, pk=pk)
    if request.method != "POST": return redirect("detalle_caso", pk=pk)
    if not caso.estado.permite_pagos:
        messages.error(request, "Pago rechazado: el estado del caso no admite pagos."); return redirect("detalle_caso", pk=pk)
    try:
        monto = Decimal(request.POST.get("monto", ""))
        if monto <= 0: raise InvalidOperation
    except (InvalidOperation, ValueError):
        messages.error(request, "Ingrese un monto válido mayor que cero."); return redirect("detalle_caso", pk=pk)
    pago = Pago(caso=caso, monto=monto, fecha=date.today(), descripcion=request.POST.get("descripcion", "Pago registrado desde el portal"))
    pago.full_clean(); pago.save(); messages.success(request, f"Pago aceptado. Total actualizado: S/ {caso.total_pagado():.2f}.")
    return redirect("detalle_caso", pk=pk)

def subir_documento(request, pk):
    expediente = get_object_or_404(Expediente, pk=pk)
    form = DocumentoExpedienteForm(request.POST, request.FILES, instance=expediente)
    if request.method == "POST" and form.is_valid(): form.save(); messages.success(request, "Documento subido correctamente.")
    else: messages.error(request, "No se pudo subir el documento.")
    return redirect("detalle_caso", pk=expediente.caso_id)

def api_caso(request, pk):
    caso = get_object_or_404(Caso.objects.select_related("cliente", "estado").prefetch_related("abogados", "expedientes"), pk=pk)
    return JsonResponse({"codigo": caso.codigo, "cliente": caso.cliente.nombres, "estado": caso.estado.nombre, "abogados": [u.get_full_name() or u.username for u in caso.abogados.all()], "numero_expedientes": caso.expedientes.count(), "total_pagado": str(caso.total_pagado())})
