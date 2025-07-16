# Despliegue

## Pre-requisitos
- Acceso a un cluster Kubernetes y `kubeconfig`
- Credenciales de Docker Registry en secretos
- Token de GitHub para el workflow

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
