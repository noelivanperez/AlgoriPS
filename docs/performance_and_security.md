# Pruebas de Rendimiento y Seguridad

Esta guía describe cómo ejecutar las distintas suites de pruebas incluidas en la Fase 7 del proyecto AlgoriPS.

## 1. Ejecución de pruebas

### Carga con Locust
```
locust -f tests/performance/locustfile.py --headless -u 60 -r 10 -t 1m
```

### Soak test
```
./tests/performance/soak_test.sh
```
Genera archivos `soak_report.csv` y `soak_report.cpu` en el mismo directorio.

### Benchmarks
```
pytest tests/benchmarks --benchmark-only
```
Los tiempos medios deben ser menores a **200 ms por archivo**.

### SAST y dependencias
```
bandit -r .
pip-audit -r requirements.txt
```

### Pruebas de penetración
```
./scripts/pen_test.sh
```
El resultado se guarda en `scripts/security_scan.txt` y los hallazgos en `docs/security_audit.md`.

## 2. Interpretación de reportes y umbrales
- **Locust**: revisar el archivo CSV generado. El tiempo de respuesta promedio no debe degradarse significativamente a lo largo del tiempo.
- **Soak test**: verificar que el uso de CPU y memoria sea estable durante las 4 horas.
- **Benchmarks**: si las medias superan los 200 ms por archivo, optimizar el código.
- **Bandit/pip-audit**: si se reportan vulnerabilidades de severidad *High* o superior, la build fallará.
- **Pen-test**: registrar vulnerabilidades en `docs/security_audit.md` y corregirlas.

## 3. Acciones correctivas
1. Optimizar funciones críticas y aplicar caching si es necesario.
2. Actualizar dependencias vulnerables o aplicar parches.
3. Revisar configuraciones de seguridad del servidor y aplicar hardening.
