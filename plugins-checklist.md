# Checklist de Fase 5 – Arquitectura de Plugins y Extensibilidad

- [x] Definir contrato de plugin en `core/plugins/contract.py`:
  - Clase abstracta `BasePlugin` con métodos obligatorios: `name()`, `version()`, `register(cli, gui_registry)`
  - Documentar argumentos y dependencias de cada plugin.
- [x] Implementar gestor de plugins en `core/plugins/manager.py`:
  - Escaneo dinámico de carpetas `/plugins/**/`
  - Llamada a `register()` de cada plugin
  - Soporte para activar/desactivar plugins en caliente
- [x] Escribir pruebas unitarias en `tests/test_plugin_manager.py` para todas las funciones de `PluginManager`
- [x] Extender CLI (`cli/main.py`) con subcomandos:
  - `algorips plugin list`
  - `algorips plugin install <ruta_o_URL>`
  - `algorips plugin uninstall <nombre>`
  - Documentar cada acción en `--help`
- [x] Añadir pestaña **Plugins** en la GUI (`gui/src/features/plugins`):
  - Listado de plugins con nombre, versión y toggle ON/OFF
  - Formulario “Instalar plugin” para ZIP o carpeta local
  - Botón “Ver documentación” que abra el README del plugin
- [x] Desarrollar **tres ejemplos de plugins** en `/plugins`:
  - `ts-analyzer/` (análisis de TypeScript)
  - `eslint-plugin/` (integración con ESLint)
  - `rag-markdown/` (RAG sobre Markdown)
  - Cada uno con su `setup.py` o `pyproject.toml`, `README.md` y tests en `tests/plugins/`
- [x] Escribir tests unitarios en `tests/plugins/` para cada ejemplo de plugin
- [x] Crear pruebas de integración en `tests/integration/test_plugins_flow.py` que:
  1. Instalen y activen un plugin
  2. Ejecuten un análisis usando el plugin
  3. Desactiven y desinstalen el plugin
  4. Verifiquen que el core vuelve a comportarse sin el plugin
- [x] Actualizar CI (GitHub Actions) para:
  - Instalar dependencias de plugins
  - Ejecutar suite de `core/plugins` y `tests/plugins` e integración
- [x] Documentar en `docs/plugins.md`:
  1. Arquitectura de plugins y flujo de registro
  2. Guía paso a paso para crear un plugin nuevo
  3. Uso de comandos `plugin list/install/uninstall` en CLI y GUI
  4. Ejemplos y capturas de pantalla
- [x] **Validación general**: ejecutar todas las pruebas unitarias y de integración, corregir errores detectados y optimizar rendimiento donde sea necesario

