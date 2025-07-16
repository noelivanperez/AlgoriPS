# Fase 3 – Uso y Pruebas de Insights Semánticos

## Objetivo de la fase
Procesar el análisis profundo del código y representar la información semántica en la GUI.

## Requisitos Previos
- Fase 2 completada y GUI funcionando.

## Instalación y Configuración
1. Ejecutar el comando para análisis profundo:
   ```bash
   algorips analyze --deep
   ```
   El resultado se guarda como JSON y puede cargarse en la GUI.

## Guía de Uso
- Abrir la pestaña **Semantic Insights** en la aplicación.
- Navegar el grafo de dependencias y seleccionar nodos para ver detalles.
- Aplicar parches propuestos desde la interfaz.

## Ejecución de Pruebas
Los tests semánticos se encuentran en `core/semantic` y se ejecutan con:
```bash
pytest
```

## Resultados Esperados
- Se genera un JSON semántico con relaciones de código.
- La GUI permite explorar interactivamente dicho grafo.
- Las pruebas en `core/semantic` deben completarse sin fallos.


