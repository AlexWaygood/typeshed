import importlib.readers
import types

class ModuleSpec: ...
class BuiltinImporter: ...
class FrozenImporter: ...
class WindowsRegistryFinder: ...
class FileFinder: ...
class SourcelessFileLoader: ...
class ExtensionFileLoader: ...
class NamespaceLoader:
    def get_resource_reader(self, module: types.ModuleType) -> importlib.readers.NamespaceReader: ...
