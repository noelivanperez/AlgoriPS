# Fase 1 – Uso y Pruebas

## Objetivo de la fase
Configurar la base del proyecto y exponer un CLI inicial para analizar código de forma local.

## Requisitos Previos
- Python 3.10+
- Docker y Docker Compose

## Instalación y Configuración
1. Copiar `.env.example` a `.env` y ajustar credenciales.
2. Levantar los servicios necesarios:
   ```bash
   docker compose up -d
   ```
3. Crear entorno virtual e instalar dependencias:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Guía de Uso
- Inicializar configuración en un proyecto:
  ```bash
  python -m algorips init
  ```
- Ejecutar análisis básico:
  ```bash
  python -m algorips analyze /ruta/al/proyecto
  ```

## Ejecución de Pruebas
Lanzar todas las pruebas unitarias del núcleo:
```bash
pytest -q
```

## Resultados Esperados
- Se generan archivos de configuración iniciales.
- El comando `analyze` produce un resumen JSON con métricas básicas.
- Todas las pruebas deben finalizar exitosamente.


