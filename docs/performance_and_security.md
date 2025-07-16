# Rendimiento y Seguridad

Esta sección resume los resultados de las pruebas de rendimiento y seguridad.

## Resultados
- Las pruebas de rendimiento muestran tiempos de respuesta menores a 200ms para `/healthz`.
- No se encontraron vulnerabilidades críticas en la última auditoría de dependencias.

## Cómo interpretar los reportes
- **Tiempos de respuesta**: valores más bajos indican un sistema más rápido.
- **Vulnerabilidades**: si `pip-audit` lista paquetes con severidad alta, conviene actualizarlos de inmediato.

## Repetir las pruebas localmente
1. Instala las dependencias con `pip install -r requirements.txt` y `pip install pip-audit`.
2. Ejecuta `pytest tests/performance` para las pruebas de velocidad.
3. Ejecuta `pip-audit` para revisar vulnerabilidades.
4. Consulta los resultados en la terminal y compara con los de este documento.
