import importlib.util
from pathlib import Path
from typing import Callable, Any

from paletted.palette import ColorParser

class ApplierLoader:
  def __init__(self, color_parser: ColorParser, wallpaper_path: Path, appliers_dir: Path) -> None:
    self.color_parser = color_parser
    self.wallpaper_path = wallpaper_path
    self.appliers_dir = appliers_dir

  def run_custom_applier(self, applier_name: str) -> None:
    file_path = self.appliers_dir / f"{applier_name}.py" 

    if not file_path.exists():
      raise FileNotFoundError(f"Applier file not found: {file_path}")

    module_name = f"custom_applier.{file_path.stem}"

    try:
      spec = importlib.util.spec_from_file_location(module_name, file_path)
      if spec is None or spec.loader is None:
        raise ImportError(f"Failed to create module specification for {file_path}")

      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)

      applier_func: Callable[..., Any] | None = getattr(module, applier_name, None)
      
      if applier_func is None:
        raise AttributeError(f"Function '{applier_name}' not found in file {file_path}")

      applier_func(self.color_parser.parse_placeholder, self.wallpaper_path)

    except Exception as e:
      print(f"Error executing custom applier {file_path.name}: {e}")