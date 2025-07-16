# Plugins en AlgoriPS

Esta fase introduce un sistema de extensibilidad mediante plugins. Cada plugin debe implementar la clase `BasePlugin` y registrar sus comandos o vistas a través del `PluginManager`.

## Crear un plugin

1. Crear una carpeta dentro de `plugins/` con un archivo `__init__.py` que defina la clase `Plugin`.
2. Implementar los métodos `name()`, `version()` y `register(cli, gui_registry)`.
3. Opcionalmente añadir `setup.py` o `pyproject.toml` para gestionar dependencias.
4. Añadir pruebas en `tests/plugins/`.

## Comandos CLI

- `algorips plugin list` – muestra los plugins instalados.
- `algorips plugin install <ruta>` – instala un plugin desde una carpeta o ZIP.
- `algorips plugin uninstall <nombre>` – elimina un plugin.

## GUI

La pestaña **Plugins** permite ver los plugins disponibles, instalarlos desde un formulario y abrir su documentación.
