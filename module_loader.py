import importlib
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ModuleLoader:
    """
    Dynamically loads modules from various domains and handles their integration.
    
    Attributes:
        modules (Dict[str, Any]): Dictionary to store loaded modules.
        module_path (str): Path where modules are located.
        
    Methods:
        load_module: Loads a specific module by name with error handling.
        reload_modules: Reloads all modules in case of updates or errors.
    """
    
    def __init__(self):
        self.modules = {}
        self.module_paths = ["perception", "reasoning", "memory"]
        
    def _import_module(self, module_name: str) -> Any:
        """
        Imports a module with error handling and logging.
        
        Args:
            module_name (str): Name of the module to import.
            
        Returns:
            Any: The imported module or None if failed.
        """
        try:
            logger.info(f"Attempting to load module: {module_name}")
            module = importlib.import_module(module_name)
            return module
        except ImportError as e:
            logger.error(f"Failed to import module {module_name}: {str(e)}")
            raise ModuleImportError(f"Module {module_name} not found or failed to import") from e
    
    def load_modules(self) -> Dict[str, Any]:
        """
        Loads all modules from specified paths.
        
        Returns:
            Dict[str, Any]: Dictionary of loaded modules.
            
        Raises:
            ModuleLoadError: If any module fails to load.
        """
        try:
            for path in self.module_paths:
                logger.info(f"Processing module path: {path}")
                module = self._import_module(path)
                if module:
                    self.modules[path] = module
                    logger.info(f"Successfully loaded module: {path}")
                else:
                    raise ModuleNotFoundError(f"Module at {path} failed to load")
            return self.modules
        except Exception as e:
            logger.error(f"Failed to load modules: {str(e)}")
            raise ModuleLoadError("Failed to load one or more modules") from e
    
    def reload_module(self, module_name: str) -> None:
        """
        Reloads a specific module.
        
        Args:
            module_name (str): Name of the module to reload.
            
        Raises:
            ModuleNotFoundError: If the module isn't loaded.
        """
        if module_name not in self.modules:
            raise ModuleNotFoundError(f"Module {module_name} not found")
        try:
            logger.info(f"Reloading module: {module_name}")
            importlib.reload(self.modules[module_name])
        except Exception as e:
            logger.error(f"Failed to reload module {module_name}: {str(e)}")
            raise ModuleReloadError(f"Failed to reload module {module_name}") from e

class ModuleImportError(Exception):
    """Raised when a module fails to import."""
    
class ModuleNotFoundError(Exception):
    """Raised when a module isn't found or loaded."""
    
class ModuleReloadError(Exception):
    """Raised when reloading a module fails."""

# Example usage:
if __name__ == "__main__":
    loader = ModuleLoader()
    modules = loader.load_modules()
    logger.info("Modules loaded successfully: %s", modules)