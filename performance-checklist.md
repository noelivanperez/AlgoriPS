# Checklist de Fase 7 – Pruebas de Rendimiento, Carga y Seguridad

- [x] Configurar framework de pruebas de carga en `/tests/performance/`:
  - `locustfile.py` con escenarios `scan_small_repo` (10 usuarios) y `scan_large_repo` (50 usuarios).
  - Alternativamente, escenario equivalente en JMeter.
- [x] Crear script `soak_test.sh` para ejecutar Locust en modo headless durante 4 horas y generar informe de CPU/memoria.
- [x] Implementar benchmarks con **pytest-benchmark** en `/tests/benchmarks/`:
  - `test_analyze_speed()`
  - `test_patch_apply_speed()`
  - Establecer umbrales de tiempo (< 200 ms por archivo).
- [x] Configurar **Bandit** y **pip-audit** para SAST y escaneo de dependencias:
  - Añadir `bandit .` y `pip-audit` en CI.
- [x] Crear pruebas de penetración básicas con **OWASP ZAP** o **Nikto**:
  - Script de escaneo contra el endpoint HTTP local.
  - Documentar hallazgos en `docs/security_audit.md`.
- [x] Añadir workflow de GitHub Actions `security-performance.yml` que:
  - Ejecute locust en headless y pytest-benchmark.
  - Ejecute Bandit y pip-audit y falle la build si hay vulnerabilidades >= High.
- [x] Documentar en `docs/performance_and_security.md`:
  1. Cómo ejecutar localmente cada suite (carga, soak, benchmark, SAST, dependency scan, pen-test).
  2. Interpretación de reportes y umbrales de aceptación.
  3. Acciones correctivas ante fallos.
- [x] **Validación general**: ejecutar todos los tests de carga, benchmarks, SAST, dependency scan y pen-test; corregir errores detectados y optimizar rendimiento donde sea necesario.
