# Checklist de Fase 8 – Documentación y Soporte

- [x] Crear manual de usuario en `docs/user_manual.md` en español, con secciones:
  1. Introducción a AlgoriPS (qué es y para qué sirve)
  2. Instalación paso a paso (CLI, GUI, plugins)
  3. Tutorial básico de Docker: explicar como si fuera para un niño de 10 años
  4. Tutorial básico de GitHub Actions: explicar concepto de pipeline con un ejemplo muy simple
  5. Tutorial básico de Python, Node.js y React: qué son, para qué sirven y comandos esenciales
  6. Sección de FAQs y troubleshooting
- [x] Crear referencia de API en `docs/api_reference.md` en español, detallando:
  1. Cada endpoint HTTP/REST (ruta, método, parámetros, ejemplo request/response)
  2. Esquemas JSON (AnalysisResult, DiffFile, TestReport, SemanticGraph)
  3. Explicación para principiantes de qué es un JSON y cómo leerlo
- [x] Implementar script `scripts/generate_release_notes.py`:
  - Lee commits entre último tag y HEAD
  - Agrupa por tipo (feat, fix, docs, test, ci)
  - Genera o actualiza `release_notes.txt` y `CHANGELOG.md`
  - Añadir un comentario en el script que explique línea a línea qué hace (como para un niño)
- [x] Añadir plantillas en `.github/`:
  - `ISSUE_TEMPLATE/bug_report.md` (en español, con instrucciones claras)
  - `ISSUE_TEMPLATE/feature_request.md`
  - `PULL_REQUEST_TEMPLATE.md`
  - Cada plantilla debe incluir un breve tutorial (“¿Cómo llenar este formulario?”) en lenguaje simple
- [x] Crear guía de ejemplos en `docs/examples/` con:
  1. Ejemplo de uso CLI y GUI (capturas de pantalla o ejemplos de salida)
  2. Ejemplo de aplicación de parche semántico
  3. Ejemplo de flujo completo de PR y merge
  - Cada ejemplo con explicación paso a paso, como para un niño de 10 años
- [x] Desarrollar automatizaciones de mantenimiento en `.github/workflows/maintenance.yml`:
  - Tarea que detecte dependencias desactualizadas (`pip-audit` o similar)
  - Tarea que envíe resumen de tests fallidos a Slack/Email
  - Documentar cada workflow inline con comentarios sencillos
- [x] Crear `docs/contributing.md` en español:
  1. Cómo reportar bugs y proponer features
  2. Cómo clonar el repo, crear ramas y enviar PR
  3. Glosario de términos (commit, branch, PR) explicado para novatos
- [x] Documentar en `docs/performance_and_security.md`:
  - Resumen de resultados de pruebas de rendimiento y seguridad
  - Cómo interpretar los reportes
  - Pasos para repetir las pruebas localmente (explicado paso a paso)
- [x] **Validación general**: ejecutar el script de release notes, revisar que todas las plantillas y documentos se abren correctamente, y corregir cualquier error o inconsistencia detectada.

