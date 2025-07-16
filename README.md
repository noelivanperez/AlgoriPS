# AlgoriPS

AlgoriPS aims to provide a local AI assistant for code analysis and refactoring. The
project integrates an Ollama LLM, MySQL for persistent storage, and a modular CLI.

## Development

Requirements are listed in `requirements.txt`. A Docker Compose file is provided to
start services for MySQL, Adminer, and Ollama.

Activate the virtual environment and install dependencies::

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Run the CLI::

    python -m algorips --help

Run tests with::

    pytest
