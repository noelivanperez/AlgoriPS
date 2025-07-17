# Despliegue

## Pre-requisitos
- Acceso a un cluster Kubernetes y `kubeconfig`
- Credenciales de Docker Registry en secretos
- Token de GitHub para el workflow

## Workflows de GitHub
El repositorio incluye varios workflows en `.github/workflows` que
automatizan el ciclo de vida de la aplicación.

- **ci.yml** ejecuta `flake8` más las pruebas unitarias e de
  integración en cada *push* o *pull request*.
- **deploy.yml** construye las imágenes Docker y despliega la
  aplicación con `docker-compose.prod.yml` o los manifests de
  `k8s/`.
- **maintenance.yml** se ejecuta semanalmente para correr
  `pip-audit` y `bandit`, enviando una alerta a Slack si algo falla.

## Despliegue a staging y producción
1. Construir imágenes y subirlas:
   ```bash
   docker build -f docker/Dockerfile.core -t myregistry/algorips-core:latest .
   docker push myregistry/algorips-core:latest
   ```
2. Aplicar manifests:
   ```bash
   kubectl apply -f k8s/
   ```
3. Verificar que los pods estén en ejecución:
   ```bash
   kubectl get pods
   ```

## Uso del script de rollback
Ejecutar indicando el tag deseado:
```bash
./scripts/rollback.sh v1.2.3
```

## Métricas y dashboards
- Prometheus lee la configuración en `monitoring/prometheus.yml`.
- Grafana carga dashboards desde `monitoring/grafana/`.
Acceder a `http://<grafana>/` con las credenciales configuradas.
