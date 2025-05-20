**Billchemy: Generador de Facturas con Clean Architecture**

Este proyecto es una API construida con **FastAPI**, diseñada para generar y gestionar plantillas de factura (.docx/.html) siguiendo los principios de **Clean Architecture** y un flujo de trabajo mantenible y testeable.

---

## 📦 Estructura del Proyecto

```text
billchemy/
├── .github/                     # Configuración de CI (GitHub Actions)
├── src/                         # Código fuente
│   ├── app/                     # Inicialización de FastAPI
│   ├── domain/                  # Entidades, Value Objects, Puertos (interfaces de dominio)
│   ├── usecases/                # Casos de uso: lógica de aplicación
│   ├── interfaces/              # Contratos de frontera (controllers)
│   ├── adapters/                # Implementaciones de puertos: repos, PDF, integraciones
│   ├── schemas/                 # Modelos Pydantic de request/response
│   ├── dependencies.py          # Wiring de dependencias
│   └── templates/               # Plantillas Jinja2 / repositorio de facturas                      # Pruebas unitarias e integración
├── pyproject.toml               # Configuración de Poetry y metadatos
├── poetry.lock                  # Versión exacta de dependencias
├── mypy.ini                     # Configuración de MyPy
├── .flake8                      # Configuración de Flake8
├── .pre-commit-config.yaml      # Hooks de pre-commit: Black, Flake8, MyPy, YAML
├── main.py                      # Entry-point para Uvicorn
└── README.md                    # Este archivo
```

---

## 🛠️ Prerrequisitos

* **Python 3.12+** instalado.
* **Poetry** para gestión de dependencias.
* (Opcional) **Docker** y **docker-compose** si prefieres contenedores.

---

## ⚙️ Creación del Entorno

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/tu-usuario/billchemy.git
   cd billchemy
   ```

2. **Instalar dependencias con Poetry**:

   ```bash
   poetry install
   ```

3. **Activar el entorno virtual** (si Poetry no lo activa automáticamente):

   ```bash
   poetry shell
   ```
   o

   ```bash
   source .venv/bin/activate
   ```

---

## 🚀 Ejecución Local

1. **Arrancar la aplicación**:

   ```bash
   uvicorn main:app --reload
   ```
2. **Abrir en el navegador**:
   Visita [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver la documentación generada por OpenAPI y probar los endpoints.

---

## 💡 Endpoints Principales

* **`POST /api/v1/invoices/templates/upload`**: Recibe un archivo `.docx` o  y lo guarda como plantilla.
* **`GET  /api/v1/invoices/templates`**: Lista las plantillas disponibles.
* **`POST /api/v1/invoices/generate`**: Genera un PDF de factura a partir de una plantilla y datos JSON.

> *Consultar el auto-generated docs para todos los detalles y esquemas*

---

## 🏗️ Arquitectura Clean

1. **Domain**: Entidades (`Invoice`, `InvoiceItem`), Value Objects (`InvoiceID`, `Money`) y puertos de dominio (`TemplateRepository`, `PDFGenerator`).
2. **Use Cases**: Clases que orquestan la lógica de aplicación (`SaveTemplate`, `ListTemplates`, `GenerateInvoice`).
3. **Interfaces**: Contratos de frontera para controladores HTTP (`InvoiceController`).
4. **Adapters**: Implementaciones concretas usando FastAPI, filesystem, Jinja2+WeasyPrint, python-docx.
5. **App**: Inyección de dependencias (`dependencies.py`) y registro de routers en `app/main.py`.

---

## 🧪 Pruebas

* **Unitarias** con `pytest` en `src/tests/`:

  ```bash
  poetry run pytest -v
  ```
* **Cobertura**:

  ```bash
  poetry run pytest
  ```

---

## 🎯 Buenas Prácticas Integradas

* **Tipado estático** con MyPy (`mypy.ini`).
* **Linting y formateo** con Black y Flake8 (`.flake8`, `pre-commit`).
* **Pre-commit hooks** para asegurar calidad antes de cada commit.
* **CI** en GitHub Actions: linting, type-checking e instalación de dependencias.

---

## ⚙️ Requisitos del Sistema

Para poder convertir las plantillas .docx a PDF, tu entorno debe contar con LibreOffice en modo headless. Asegúrate de que el binario soffice (o libreoffice) está disponible en el PATH.
Instalación

    Ubuntu / Debian

* **de igual manera puedes ejecutar el docker para poder tener acceso al proyecto

   1. ejecutar :

   ```bash
   docker-compose up -d billchemy
   ```
   2. acceder a la url localhost:8000


## 📖 Contribuciones

¡Bienvenidas! Abre un issue o un pull request. Sigue el estilo de commit `feat:`, `fix:`, etc., y asegúrate de que todos los hooks de pre-commit pasen antes de enviar.

---



*Billchemy* © 2025
