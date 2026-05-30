from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, ValidationError
import json
import os

from paletted.exceptions import StateError


class StateModel(BaseModel):
  wallpaper: Path
  wallpaper_type: str

class StateManager:
  def __init__(self, app_name: str = "paletted") -> None:
    self.app_name = app_name
    self.cache_dir = self._get_cache_dir()
    self.state_file = self.cache_dir / "state.json"

  def _get_cache_dir(self) -> Path:
    xdg_cache = os.environ.get("XDG_CACHE_HOME")
    if xdg_cache:
      base_cache = Path(xdg_cache)
    else:
      base_cache = Path.home() / ".cache"

    path = base_cache / self.app_name
    path.mkdir(parents=True, exist_ok=True)
    return path

  def save_state(self, wallpaper_path: Path, wallpaper_type: str) -> StateModel | None:
    state = {
      "wallpaper": str(wallpaper_path.resolve()),
      "wallpaper_type": wallpaper_type,
      "updated_at": datetime.now().isoformat(),
    }

    with open(self.state_file, "w", encoding="utf-8") as f:
      json.dump(state, f, indent=2, ensure_ascii=False)

  def load_state(self) -> StateModel:
    if not self.state_file.exists():
      raise FileNotFoundError("State file is not exists")

    try:
      with open(self.state_file, "r", encoding="utf-8") as f:
        return StateModel.model_validate(json.load(f))
    except (json.JSONDecodeError, IOError, ValidationError):
      self.state_file.unlink(missing_ok=True)
      raise StateError("State file is invalid")
