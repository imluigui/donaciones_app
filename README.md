# Sistema de Gestión de Donaciones

Sistema de gestión de recursos y donaciones de alimentos entre empresas y organizaciones sociales.

## Requisitos Previos

- Python 3.13+
- `pip`

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/imluigui/donaciones_app.git
   cd donaciones_app
   ```

2. Crear y activar un entorno virtual:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
# Asegúrate de estar en el directorio raíz del proyecto
./venv/Scripts/python -m uvicorn app.main:app --reload
```

Accede a `http://127.0.0.1:8000` en tu navegador.

## Tests

Para ejecutar las pruebas:

```bash
./venv/Scripts/python -m pytest
```
