from django import forms
from .models import Cliente, Expediente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ("nombres", "documento", "telefono", "correo")

class DocumentoExpedienteForm(forms.ModelForm):
    class Meta:
        model = Expediente
        fields = ("documento",)
