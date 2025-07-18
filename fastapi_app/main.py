from fastapi import FastAPI
from pydantic import BaseModel

from algorips.core.git import local
from algorips.core.plugins import PluginManager

app = FastAPI(title="AlgoriPS API")

pm = PluginManager()

class CloneRequest(BaseModel):
    url: str
    dest: str

class BranchRequest(BaseModel):
    name: str

class CommitRequest(BaseModel):
    message: str

class InstallRequest(BaseModel):
    path: str

@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}

@app.post("/repo/clone")
def clone_repo(req: CloneRequest) -> dict[str, str]:
    """Clone a repository."""
    local.clone(req.url, req.dest)
    return {"status": "cloned"}

@app.post("/repo/branch")
def create_branch(req: BranchRequest) -> dict[str, str]:
    """Create and checkout a new branch."""
    local.checkout_branch(req.name, create=True)
    return {"status": "created"}

@app.post("/repo/commit")
def commit_changes(req: CommitRequest) -> dict[str, str]:
    """Commit all changes."""
    local.commit_all(req.message)
    return {"status": "committed"}

@app.get("/plugins")
def list_plugins() -> list[dict[str, object]]:
    """Return installed plugins."""
    return list(pm.list_plugins())

@app.post("/plugins/install")
def install_plugin(req: InstallRequest) -> dict[str, str]:
    """Install a plugin from a path."""
    pm.install(req.path)
    return {"status": "installed"}

@app.delete("/plugins/{name}")
def uninstall_plugin(name: str) -> dict[str, str]:
    """Uninstall a plugin by name."""
    pm.uninstall(name)
    return {"status": "removed"}
