#!/bin/bash
# Setup script for AlgoriPS
set -e

# 1. Verify dependencies
check_command() {
  cmd="$1"
  ver="$2"
  name="$3"
  if ! command -v "$cmd" >/dev/null; then
    echo "Error: $name >= $ver is required" >&2
    exit 1
  fi
}

check_command python3 3.10 Python
check_command node 18 Node.js

# Ensure python version
PY_MAJ=$(python3 -c 'import sys; print(sys.version_info[0])')
PY_MIN=$(python3 -c 'import sys; print(sys.version_info[1])')
if [ "$PY_MAJ" -lt 3 ] || { [ "$PY_MAJ" -eq 3 ] && [ "$PY_MIN" -lt 10 ]; }; then
  echo "Error: Python >=3.10 required" >&2
  exit 1
fi

NODE_MAJ=$(node -v | sed 's/v//' | cut -d'.' -f1)
if [ "$NODE_MAJ" -lt 18 ]; then
  echo "Error: Node.js >=18 required" >&2
  exit 1
fi

# 2. Python virtualenv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. GUI installation and fixes
cd gui
npm install

# Ensure package.json main points to main.js
if grep -q '"main"' package.json; then
  sed -i 's/"main"[^"]*"[^"]*"/"main": "main.js"/' package.json
else
  sed -i '1a\  "main": "main.js",' package.json
fi

# Create index.js if missing
if [ ! -f index.js ]; then
  cat <<'JS' > index.js
// gui/index.js
require('./main.js');
JS
fi
cd ..

# 4. MySQL configuration
cat > .env <<'ENV'
DB_HOST=localhost
DB_USER=root
DB_PASS=sasa
DB_NAME=algorips
ENV

echo "CREATE DATABASE IF NOT EXISTS algorips;" | mysql -u root -psasa
echo "USE algorips; CREATE TABLE IF NOT EXISTS algorips (id INT AUTO_INCREMENT PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);" | mysql -u root -psasa

# 5. Start services
ollama serve --port 11434 &
python -m algorips.main serve &

# 6. Tests
python -m algorips.cli.main analyze .
pytest --cov=algorips --cov-fail-under=90

# 7. CI workflow
mkdir -p .github/workflows
cat > .github/workflows/ci.yml <<'YAML'
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
        working-directory: gui
      - run: npm test
        working-directory: gui
      - run: python -m pip install -r requirements.txt
      - run: pytest --cov=algorips
      - uses: actions/upload-artifact@v3
        with:
          name: coverage
          path: .coverage
YAML

# 8. Vault CLI setup and example
if ! command -v vault >/dev/null; then
  echo "Installing Vault CLI..."
  sudo apt-get update && sudo apt-get install -y vault || true
fi
if [ -f .env.enc ]; then
  echo "Decrypting .env.enc with Vault"
  vault kv get -field=.env secret/algorips > .env
fi

# 9. Hello world plugin
mkdir -p plugins/hello-world
cat > plugins/hello-world/hello.py <<'PY'
print("hello-world: Plugin cargado")
PY

# 10. Performance test
cat > tests/performance_test.py <<'PY'
import time
from pathlib import Path
from algorips.core.analyzer import CodeAnalyzer

def test_large_repo_latency():
    repo = Path('tests/performance/data/large_repo')
    files = list(repo.glob('*.py'))
    start = time.perf_counter()
    CodeAnalyzer().scan(str(repo))
    elapsed = time.perf_counter() - start
    assert elapsed / len(files) <= 0.1, f"Latency {elapsed/len(files):.3f}s > 0.1s per file"
PY

# 11. Documentation
mkdir -p docs
cat > docs/fase-1.md <<'MD'
# Fase 1

## Objetivos
- Configurar la base del proyecto y el flujo CI
- Implementar analizador y GUI inicial

## Historias de Usuario
- Como desarrollador quiero analizar mi código para obtener métricas.
- Como usuario deseo gestionar plugins de manera dinámica.

## Requisitos Funcionales
- CLI para análisis y gestión de repositorios.
- GUI con navegación básica y carga de plugins.

## Entregables
- Código fuente y documentación
- Informe de cobertura de pruebas

## Cronograma
1. Semana 1: configuración entorno
2. Semana 2: desarrollo funcionalidades
3. Semana 3: pruebas y documentación
MD

# 12. Metrics in server already exposed via /metrics
# 13. Permissions
chmod +x setup.sh
echo "✅ AlgoriPS levantado:
  • API en http://localhost:8000
  • GUI en http://localhost:3000
  • Ollama en puerto 11434"

