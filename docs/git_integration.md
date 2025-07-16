# Git Integration

AlgoriPS uses simple wrappers around the Git CLI y la API de GitHub.

## Requisitos

- Tener configurado `git` y acceso por SSH o token.
- Para operaciones de GitHub se requiere un token personal (`GITHUB_TOKEN`).

## Flujos Básicos

1. **Clonación**: `algorips repo clone <url> --dest path`
2. **Ramas**: `algorips repo branch <name>` para crear y hacer checkout.
3. **Commits**: `algorips repo commit "mensaje"` guarda todos los cambios.
4. **Pull Requests**:
   - Crear: `algorips repo pr create --owner user --repo repo "titulo"`
   - Listar desde la GUI.
   - Hacer merge: `algorips repo pr merge <num>`

La GUI cuenta con una pestaña *Repository* que permite realizar estas acciones a través de formularios sencillos.
