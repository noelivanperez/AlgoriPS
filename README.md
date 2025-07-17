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
