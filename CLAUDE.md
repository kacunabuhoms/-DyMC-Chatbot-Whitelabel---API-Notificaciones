# Chatbot Whitelabel - API Notificaciones

## 🎯 Descripción
Servicio interno basado en FastAPI para la recepción, enriquecimiento y registro dinámico de webhooks. El sistema procesa payloads variables, los aplana para auditoría en Google Sheets y dispara notificaciones vía WhatsApp (Meta API).

## 📦 Stack Tecnológico
- **Runtime:** Python 3.10+
- **Framework:** FastAPI
- **Arquitectura:** Clean Architecture
- **Persistencia:** Google Sheets API v4 (Aplanamiento dinámico)
- **Integraciones:** Meta Business API (WhatsApp Cloud API), HTTPX/Requests.

## 📁 Estructura de Carpetas (Clean Architecture)
```
src/
  domain/         # Entidades de negocio y modelos lógicos
  application/    # Casos de uso (Orquestación: recibir -> aplanar -> enriquecer -> notificar)
  infrastructure/ # Implementaciones técnicas (Sheets Adapter, Meta Client, API Clients)
  interfaces/     # Entrypoints (FastAPI Routes, Pydantic Schemas, Middlewares)
tests/            # Pruebas unitarias y de integración
config/           # Configuración (Pydantic Settings, Variables de Entorno)

```

## 📋 Convenciones de Código

* **Estilo:** PEP8 estricto (snake_case para todo, excepto Clases en PascalCase).
* **Tipado:** Type Hints obligatorios en todas las funciones y métodos.
* **Async:** Toda operación de red (APIs, Sheets) debe ser `async/await`.
* **Errores:** Gestión de excepciones en la capa de Application para evitar fugas de infraestructura.

## 📨 Payload de Entrada (Sistema Búho)

El webhook recibe órdenes del sistema interno "Búho". El campo `shipments` es un array — se genera una fila por elemento. Ejemplo real:

```json
{
    "buho_order_id": 1000000,
    "order_id": "0000001",
    "order_ref": "REF00001",
    "order_status": "Orden Surtida",
    "order_status_id": "order_completed",
    "carrier": "Paquetexpress",
    "shipments": [
        {
            "tracking_number": "123456788",
            "status": "En ruta",
            "status_id": "started",
            "last_update": "2024-06-27 12:03:03",
            "carrier": "Paquetexpress"
        }
    ]
}
```

Los campos de `shipments` se aplanan con prefijo: `shipments.tracking_number`, `shipments.status`, etc.

## 🔐 Credenciales Google (ADC)

- **Cloud Run:** La Service Account se asigna directamente al servicio. No se necesita archivo — Google lo resuelve automáticamente.
- **Local:** Colocar `service-account.json` en la raíz del proyecto y definir `GOOGLE_APPLICATION_CREDENTIALS=service-account.json` en `.env`. Este archivo está en `.gitignore` y nunca se commitea.
- **No usar** `GOOGLE_CREDENTIALS_PATH` ni cargar archivos manualmente en el código.

## 🗺️ Fases de Desarrollo

- **Fase 1 (actual):** Recibir webhook → Aplanar JSON → Guardar en Google Sheets.
- **Fase 2 (pendiente):** Enviar notificaciones WhatsApp vía Meta Cloud API al cliente final.

## 📊 Reglas de Registro en Google Sheets

**URL:** https://docs.google.com/spreadsheets/d/1HTSVjhWc3iqs6uViCOQd_HaMT6Jjy76aYBWikVnsqDI/edit

El registro debe ser **dinámico y autodirigido** mediante la lógica de "Flattening":

1. **Aplanamiento (JSON Flattening):**
* Variables simples: Se registran con su nombre de llave (ej: `order_id`).
* Variables anidadas: Se usa notación de punto (ej: `shipments.status`, `customer.address.city`).


2. **Manejo de Listas (Arrays):**
* Si el JSON contiene una lista (ej: `shipments`), se genera **una fila independiente por cada elemento** de la lista.
* Los datos globales del JSON se repiten en cada una de estas filas.


3. **Gestión Dinámica de Columnas (Headers):**
* El sistema debe leer la Fila 1 del Sheet para identificar los encabezados existentes.
* **Si una variable no tiene columna:** Crear automáticamente el header al final de la fila 1.
* **Si el header existe:** Insertar el valor en la columna correspondiente.
* Si un valor es nulo o no existe en el JSON, la celda queda vacía.



## ⚡ Comandos Principales

```
uvicorn src.interfaces.main:app --reload  # Servidor de desarrollo
pytest                                    # Ejecutar suite de pruebas
pip install -r requirements.txt           # Instalación de dependencias

```

## 🚨 Reglas Críticas

* ✅ **Clean Architecture:** No instanciar clientes de infraestructura directamente en las rutas. Usar inyección de dependencias o capas de aplicación.
* ✅ **Performance:** El guardado en Sheets y el envío a Meta DEBEN ser `BackgroundTasks` para no retrasar la respuesta 200 OK al Webhook.
* ✅ **Escalabilidad:** El código de aplanamiento debe ser recursivo para soportar cualquier nivel de anidación.
* ❌ **Secrets:** Prohibido subir tokens de Meta o credenciales de Google al repositorio. Usar `.env`.
* ❌ **Hardcoding:** No definir nombres de columnas estáticos en el código.

## 🔗 Documentación Adicional

* [Documentación Meta API](https://developers.facebook.com/docs/whatsapp/cloud-api)
* [Referencia Google Sheets API](https://developers.google.com/sheets/api/reference/rest)

## 💬 Usar en Claude Code

Menciona siempre: "Refiere a CLAUDE.md. [tu tarea]"

```