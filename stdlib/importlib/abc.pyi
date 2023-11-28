import types
from importlib.machinery import ModuleSpec

def create_module(self, spec: ModuleSpec) -> types.ModuleType | None: ...
