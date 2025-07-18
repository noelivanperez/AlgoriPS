# AlgoriPS

AlgoriPS aims to provide a local AI assistant for code analysis and refactoring. The
project integrates an Ollama LLM, MySQL for persistent storage, and a modular CLI.

## Pre-requisitos

* Python 3.10 o superior
* Docker y Docker Compose

## Workflows CI/CD
La carpeta `.github/workflows` contiene los flujos de trabajo que
automatizan la validación y el despliegue del proyecto.
- **ci.yml** ejecuta `flake8` y las pruebas unitarias e
  integrales por cada *push* o *pull request*.
- **deploy.yml** construye las imágenes Docker y publica la
  aplicación con `docker-compose.prod.yml` o los manifests de
  Kubernetes.
- **maintenance.yml** corre semanalmente `pip-audit` y `bandit`,
  enviando una alerta a Slack si aparecen vulnerabilidades.

## Comandos Docker

Copie primero el archivo de ejemplo de variables de entorno y luego inicie los
servicios de base de datos y Ollama::

    cp .env.example .env
    docker compose up -d

You can switch the Ollama model by editing the `OLLAMA_MODEL` variable inside
`.env`. The default is `llama3`.

Para detener todos los servicios::

    docker compose down

## Desarrollo

Requirements are listed in `requirements.txt`. A Docker Compose file is provided to
start services for MySQL, Adminer, and Ollama. Copy `.env.example` to `.env` and
adjust values before running the stack.

### Variables de entorno de la base de datos

El archivo `.env` acepta ahora opciones para el pool de conexiones:

* `MYSQL_POOL_SIZE` define el tamaño del pool (valor por defecto `5`).
* `MYSQL_POOL_TIMEOUT` establece el tiempo máximo de espera en segundos para
  obtener una conexión (valor por defecto `30`).

Si en producción se requiere ajustar el pool, modifique estas variables y
reinicie la aplicación. No se necesitan migraciones adicionales.

Activate the virtual environment and install dependencies::

    python -m venv .venv
    .\.venv\Scripts\Activate
    pip install -r requirements.txt

Database migrations are stored as SQL files under `db/migrations`. Use the
helper script `scripts/init_db.py` to create the database and apply all
migrations automatically::

    python scripts/init_db.py

Run the CLI::

    python -m algorips --help

## Ejemplos de uso CLI

Inicialice una configuración por defecto en el directorio actual::

    python -m algorips init

Ejecute el análisis de código en un directorio::

    python -m algorips analyze path/to/project

Run tests with::

    pytest

Interact directly with Ollama::

    python -m algorips ollama chat "Hola" --model llama3

## Repository CLI

Clone and manage repositories::

    python -m algorips repo clone https://github.com/user/repo.git --dest myrepo
    python -m algorips repo branch feature1
    python -m algorips repo commit "add feature"
    python -m algorips repo pr create --owner user --repo repo --token TOKEN "My PR"
    python -m algorips repo pr merge 1 --owner user --repo repo --token TOKEN

## HTTP API Endpoints

Repository operations are exposed by the Flask server:
- `POST /repo/clone` with `{url, dest}`
- `POST /repo/branch` with `{name}`
- `POST /repo/commit` with `{message}`
- `GET  /repo/pr` returns open pull requests
- `POST /repo/pr/create` creates a pull request
- `POST /repo/pr/merge` with `{number}` merges a PR

Plugin management endpoints:
- `GET  /plugins` returns installed plugins
- `POST /plugins/install` with `{path}` installs a plugin
- `DELETE /plugins/<name>` removes a plugin
- Plugin documentation can be retrieved from `/plugins/<name>/README.md`

## Web Scraper Configuration

The ``scrape`` command reads a YAML file describing targets::

    targets:
      - url: http://example.com
        selectors:
          title: h1
          heading: div.wrapper h1

PyYAML is used to parse this configuration. If PyYAML is not available, the
built-in fallback parser only understands the structure above and does not
support nested mappings or complex YAML features. Nested selectors therefore
require PyYAML.
