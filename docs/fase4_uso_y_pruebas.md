# Fase 4 – Uso y Pruebas de Integración con GitHub

## Objetivo de la fase
Manejar repositorios de GitHub desde el CLI y la GUI para crear PRs automáticamente.

## Requisitos Previos
- Token de GitHub y acceso por SSH configurado.

## Instalación y Configuración
1. Exportar la variable `GITHUB_TOKEN` y asegurarse de que la clave SSH está cargada.

## Guía de Uso
- Clonar un repositorio remoto:
  ```bash
  algorips repo clone git@github.com:usuario/proyecto.git
  ```
- Crear rama y aplicar cambios:
  ```bash
  algorips repo branch nueva-rama
  ```
- Realizar commit y abrir PR:
  ```bash
  algorips repo commit "mensaje"
  algorips repo pr
  ```
- Desde la GUI se puede seguir el estado de la PR y realizar el merge.

## Ejecución de Pruebas
Los tests de integración usan mocks de GitHub y se ejecutan con:
```bash
pytest
```

## Resultados Esperados
- Las operaciones de repositorio finalizan sin errores.
- La GUI refleja el estado de la rama y la PR creada.
- Todos los tests de integración deben pasar satisfactoriamente.


