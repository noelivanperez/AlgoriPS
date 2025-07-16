# Checklist de Fase 4 – Integración Git/GitHub

- [x] Implementar módulo `core/git/local.py` con funciones:
  - `clone(repo_url, dest_path)`
  - `checkout_branch(branch_name, create: boolean)`
  - `commit_all(message: str)`
  - `push(branch_name)`
- [x] Escribir pruebas unitarias en `tests/test_git_local.py` para cada función de `core/git/local.py`
- [x] Implementar módulo `core/git/github.py` con clase `GitHubClient(token: str)` y métodos:
  - `create_pull_request(owner, repo, head, base, title, body, reviewers, labels)`
  - `list_pull_requests(owner, repo, state)`
  - `merge_pull_request(owner, repo, pr_number)`
- [x] Escribir pruebas unitarias en `tests/test_github_client.py` para cada método de `GitHubClient`
- [x] Extender CLI (`cli/main.py`) agregando comandos:
  - `algorips repo clone <url> [--dest]`
  - `algorips repo branch <name>`
  - `algorips repo commit "<mensaje>"`
  - `algorips repo pr create [--reviewers] [--labels]`
  - `algorips repo pr merge <pr_number>`
- [x] Documentar cada comando en la ayuda (`--help`) del CLI
- [x] Añadir pestaña **Repository** en la GUI (`gui/src/features/repository`) que incluya:
  - Formulario de clonación de repositorio
  - Listado de ramas y pull requests (fetch desde API)
  - Botones para crear rama, abrir PR y hacer merge
- [x] Conectar la GUI con los nuevos endpoints en `src/utils/api.ts`
- [x] Escribir pruebas de integración completas en `tests/integration/test_repo_flow.py` simulando:
  1. Clonación de un repositorio de prueba
  2. Creación de rama y checkout
  3. Edición de un archivo dummy
  4. Commit y push
  5. Creación de pull request
  6. Merge de pull request y verificación de cierre de rama
- [x] Actualizar documentación:
  - `README.md` con ejemplos de uso CLI y GUI
  - `docs/git_integration.md` detallando requisitos (token, SSH) y flujos
- [x] Actualizar CI (GitHub Actions) para ejecutar las nuevas pruebas unitarias e integración
- [x] **Validación general**: ejecutar todas las pruebas unitarias e integración, corregir cualquier error detectado y optimizar donde sea necesario
