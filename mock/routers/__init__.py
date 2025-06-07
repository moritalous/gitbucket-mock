import os
from importlib import import_module
from pathlib import Path

from fastapi import APIRouter

# Main router to store API routers
api_router = APIRouter(prefix="/api/v3")

# Get all Python files in the routers directory
router_files = [
    f[:-3]
    for f in os.listdir(Path(__file__).parent)
    if f.endswith(".py") and f != "__init__.py"
]

# Import and register routers from each router file
for router_file in router_files:
    try:
        module = import_module(f".{router_file}", package="routers")
        if hasattr(module, "router"):
            api_router.include_router(module.router)
    except ImportError as e:
        print(f"Error importing router {router_file}: {e}")
