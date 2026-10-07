# Entrega Evaluación 02 A

## Requisitos

- Python 3.11 o superior
- Django 5.2.7 (`pip install -r requirements.txt`)

## Ejecución

```powershell
python manage.py migrate
python manage.py cargar_demo
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/casos/`. El panel administrativo está en `/admin/`.

Credenciales de demostración:

- Administrador: `admin` / `Admin2026!`
- Abogados: `mgarcia` y `jtorres` / `Abogado2026!`

## Evidencia de la ejecución

```text
System check identified no issues (0 silenced).
Ran 4 tests in 0.030s
OK
Cliente: Empresa Andina SAC (20123456789); casos: 2;
abogados de CAS-2026-001: 2; expedientes: 2; total: S/ 3550.50
```

La suite verifica el total calculado con `aggregate`/`Sum`, el bloqueo de pagos para un estado no permitido, el registro de pago por POST, la cookie `ultimo_estado` y la API JSON.

## Estructura

- `casos/models.py`: modelos y reglas de negocio.
- `casos/admin.py`: mantenedores e inlines del administrador.
- `casos/views.py`, `casos/urls.py`, `casos/forms.py`: portal, carga de documentos y API.
- `templates/`: plantilla base, portal y personalización del administrador.
- `casos/tests.py`: pruebas automatizadas.
