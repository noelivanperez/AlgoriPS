# Checklist de Fase 6 – Despliegue y Configuración en Producción

- [x] Crear Dockerfiles multi-stage en `/docker`:
  - `Dockerfile.core` (build y runtime separados)
  - `Dockerfile.gui`
  - `Dockerfile.plugins`
- [x] Definir orquestación de producción:
  - Kubernetes manifests en `/k8s`:
    - `deployment.yaml`
    - `service.yaml`
    - `configmap.yaml`
    - `secret.yaml`
  - O alternativamente `docker-compose.prod.yml` con servicios optimizados
  - Incluir `readinessProbe` y `livenessProbe`
- [x] Configurar parámetros de Ollama en producción:
  - Variables en ConfigMap: `OLLAMA_TEMPERATURE`, `OLLAMA_MAX_TOKENS`, `OLLAMA_BATCH_SIZE`
  - Límites de recursos CPU/GPU en manifest
- [x] Añadir script de rollback en `scripts/rollback.sh` para desplegar tags anteriores
- [x] Crear workflow de GitHub Actions `deploy.yml`:
  - On: push a `main`
  - Jobs:
    - build & test
    - build & push imágenes
    - deploy a staging
    - smoke tests
    - deploy a producción
- [x] Implementar monitorización y alertas:
  - Configurar Prometheus (`/monitoring/prometheus.yml`)
  - Dashboards Grafana en `/monitoring/grafana/`
  - Instrumentar endpoints `/healthz` y `/metrics` en core
  - Configurar alertas a Slack/Email
- [x] Documentar despliegue en `docs/deployment.md`:
  1. Pre-requisitos (kubeconfig, credenciales, tokens)
  2. Pasos para construir y desplegar en staging y producción
  3. Cómo usar el script de rollback
  4. Cómo acceder a métricas y dashboards
- [x] **Validación general**: ejecutar todo el pipeline de CI/CD, smoke tests y rollback; corregir errores y optimizar donde sea necesario
