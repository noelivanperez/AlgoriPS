"""Genera notas de versión usando los mensajes de commit.
Cada línea tiene un comentario que explica su función."""

import subprocess  # usamos esto para correr comandos de git
from collections import defaultdict  # para agrupar mensajes por tipo
from pathlib import Path  # para manejar archivos

# Obtener el último tag. Si falla, significa que no hay tags
try:  # intentamos ejecutar git describe
    last_tag = subprocess.check_output(
        ["git", "describe", "--tags", "--abbrev=0"]  # comando git
    ).decode().strip()  # convertimos la salida a texto
except subprocess.CalledProcessError:  # si el comando falla
    last_tag = ""  # no existe tag, empezamos desde el inicio

# Definir el rango de commits a revisar
log_range = f"{last_tag}..HEAD" if last_tag else "HEAD"  # desde tag hasta HEAD

# Obtener los mensajes de commit
commits = subprocess.check_output(
    ["git", "log", log_range, "--pretty=%s"]  # solo el asunto del commit
).decode().splitlines()  # separamos por líneas

# Agrupar los commits por tipo
changes = defaultdict(list)  # diccionario con lista por tipo
for msg in commits:  # revisamos cada mensaje
    part = msg.split(":", 1)[0]  # tomamos la palabra antes de ':'
    kind = part if part in {"feat", "fix", "docs", "test", "ci"} else "otros"  # tipo
    changes[kind].append(msg)  # guardamos el mensaje

# Construir las notas de versión
lines = [f"## Cambios desde {last_tag or 'inicio'}\n"]  # título principal
for kind, msgs in changes.items():  # para cada tipo encontrado
    lines.append(f"### {kind}\n")  # subtítulo del tipo
    for m in msgs:  # cada mensaje de ese tipo
        lines.append(f"- {m}\n")  # lo agregamos con viñeta

notes_text = "".join(lines)  # juntamos todo en un solo texto

# Guardar o actualizar archivos de notas
for file_name in ["release_notes.txt", "CHANGELOG.md"]:  # dos archivos
    path = Path(file_name)  # ruta del archivo
    old = path.read_text(encoding="utf-8") if path.exists() else ""  # lo que ya había
    path.write_text(notes_text + "\n" + old, encoding="utf-8")  # escribimos primero lo nuevo

print("Notas de versión generadas.")  # mensaje final
