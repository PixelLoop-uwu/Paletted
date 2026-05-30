import os
from pathlib import Path
import tomllib

from .schemas import Config

class ConfigLoader:
  def __init__(self, config_dir: Path | None):
    self.base_path = self._get_config_path(config_dir)
    self._visited: set[Path] = set()

  def _get_config_path(self, custom_config: Path | None) -> Path:
    if custom_config:
      return custom_config.resolve()
    
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
      return Path(xdg_config) / "paletted"
      
    return Path.home() / ".config" / "paletted"

  def _recursive_read(self, current_path: Path) -> dict:
    current_path = current_path.resolve()

    if current_path in self._visited:
      raise RuntimeError(
        f"Cyclic include detected: {current_path}"
      )

    if not current_path.exists():
      raise FileNotFoundError(
        f"Missing config: {current_path}"
      )

    self._visited.add(current_path)

    with open(current_path, "rb") as f:
      data = tomllib.load(f)

    combined: dict = {k: v for k, v in data.items() if k != "include"}

    for inc in data.get("include", []):
      target = inc.get("target")
      if not target:
        continue

      inc_path = (current_path.parent / target).resolve()
      inc_data = self._recursive_read(inc_path)

      for key, value in inc_data.items():
        if key not in combined:
          combined[key] = value
        elif isinstance(combined[key], list) and isinstance(value, list):
          combined[key].extend(value)
        elif isinstance(combined[key], dict) and isinstance(value, dict):
          combined[key] = {**value, **combined[key]}
        else:
          pass

    return combined

  def _apply_uniqueness(self, items: list, key_name: str) -> list:
    seen = {}
    for item in items:
      if isinstance(item, dict) and key_name in item:
        seen[item[key_name]] = item
      else:
        seen[id(item)] = item
    return list(seen.values())

  def load_all(self):
    raw_data = self._recursive_read(self.base_path / "config.toml")

    UNIQUE_KEYS = getattr(Config, "UNIQUE_KEYS", {})

    for field, key in UNIQUE_KEYS.items():
      if field in raw_data:
        raw_data[field] = self._apply_uniqueness(
          raw_data[field],
          key
        )

    allowed = set(Config.model_fields.keys())
    unknown = set(raw_data.keys()) - allowed

    if unknown:
      raise ValueError(
        f"Unknown config sections: {', '.join(sorted(unknown))}"
      )

    return Config.model_validate(raw_data)