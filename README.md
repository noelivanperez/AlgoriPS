# AlgoriPS

AlgoriPS aims to provide a local AI assistant for code analysis and refactoring. The
project integrates an Ollama LLM, MySQL for persistent storage, and a modular CLI.

## Development

Requirements are listed in `requirements.txt`. A Docker Compose file is provided to
start services for MySQL, Adminer, and Ollama. Copy `.env.example` to `.env` and
adjust values before running the stack::

    cp .env.example .env
    docker compose up -d

Activate the virtual environment and install dependencies::

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Database migrations are stored as SQL files under `db/migrations`. The initial
script creates a `projects` table that stores analyzed project metadata.

Run the CLI::

    python -m algorips --help

Run tests with::

    pytest
