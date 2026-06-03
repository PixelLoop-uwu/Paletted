from pathlib import Path
import time

from paletted.core import ApplierLoader, ConfigLoader, Executer, StateManager, Templater
from paletted.palette import PaletteGenerator, ColorParser
from paletted.utils import get_media_type, extract_frame


class Paletted:
  def __init__(self, config_dir: Path | None) -> None:
    self.config_loader = ConfigLoader(config_dir)
    self.state_manager = StateManager()

  def apply_theme(self, wallpaper_path: Path, source_index: int = 0) -> None:
    wallpaper_path = wallpaper_path.expanduser().resolve()

    if not wallpaper_path.exists():
      raise FileNotFoundError("Wallpapers not found")
    
    config = self.config_loader.load_all()
    wallpaper_type = get_media_type(wallpaper_path)
    target_image = Path(config.settings.source_image or "/tmp/paletted_frame.png")
    
    if wallpaper_type == "video":
      extract_frame(wallpaper_path, target_image)
    
    else:
      if config.settings.source_image:
        target_image.unlink(missing_ok=True) 
        target_image.symlink_to(wallpaper_path)
      else:
        target_image = wallpaper_path

    try:
      palette = PaletteGenerator().get_palette(target_image, source_index)

      Executer.apply_wallpaper(config.backend, wallpaper_path, wallpaper_type)
      StateManager().save_state(wallpaper_path, wallpaper_type)

      color_parser = ColorParser(palette)
      templater = Templater()
    
      for pkg in config.package:
        templater.render(self.config_loader.base_path / "templates", pkg, color_parser)

        for exec in pkg.exec_commands:
          time.sleep(0.2)

          Executer.run_hook(exec)

      applier_loader = ApplierLoader(color_parser, self.config_loader.base_path / "appliers")
      
      for applier in config.appliers:
        if not applier.applier: continue

        applier_loader.run_custom_applier(applier.applier)

      Executer.send_notification(config.notification)

    except Exception:
      raise

    finally:
      if not config.settings.source_image and wallpaper_type == "video":
        target_image.unlink(missing_ok=True)

  def restore_wallpaper(self) -> None:
    config = self.config_loader.load_all()
    state = self.state_manager.load_state()

    Executer.apply_wallpaper(config.backend, state.wallpaper, state.wallpaper_type)
