# Referencia de API de AlgoriPS

Esta sección describe los puntos de entrada HTTP disponibles y los esquemas de datos utilizados en la aplicación.

## Endpoints HTTP/REST

### `GET /healthz`
Retorna una cadena `"ok"` para confirmar que el servicio está activo.

Ejemplo de respuesta:
```json
"ok"
```

### `GET /metrics`
Devuelve métricas en formato de texto para Prometheus.

Ejemplo de respuesta (parcial):
```
# HELP algorips_requests_total Total requests
# TYPE algorips_requests_total counter
algorips_requests_total 3
```

### `POST /chat`
Envía un *prompt* a Ollama y retorna la respuesta del modelo. Se puede indicar el
modelo con el campo `model`.

Ejemplo de solicitud:
```json
{ "prompt": "Hola", "model": "llama3" }
```

## Esquemas JSON
A continuación se muestran los esquemas básicos que usa la aplicación.

### `AnalysisResult`
```json
{
  "path": "ruta/al/proyecto",
  "line_count": 123,
  "function_count": 10,
  "class_count": 2
}
```

### `DiffFile`
```json
{
  "file": "nombre_del_archivo.py",
  "diff": "--- antiguo\n+++ nuevo\n..."
}
```

### `TestReport`
```json
{
  "passed": 5,
  "failed": 0,
  "errors": []
}
```

### `SemanticGraph`
```json
{
  "nodes": ["A", "B"],
  "edges": [["A", "B"]]
}
```

## ¿Qué es un JSON?
Un JSON es como una lista de valores con pares "clave: valor". Se usa para guardar y enviar datos de forma sencilla. Para leerlo, observa cada clave y su valor; las llaves `{}` encierran objetos y los corchetes `[]` encierran listas.
