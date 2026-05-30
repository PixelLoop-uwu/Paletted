from pathlib import Path
import subprocess
import json

from paletted.exceptions import MatugenError
from .schemas import Palette

class PaletteGenerator:
  def execute_matugen(self, image_path: Path, source_index: int = 0) -> dict:
    try:
      result = subprocess.run(
        [
          "matugen", "image", str(image_path), 
          "--json", "hex", "--type", "scheme-content",
          "--source-color-index", str(source_index)
        ],
        capture_output=True,
        text=True,
        check=True
      )
      return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
      error_msg = e.stderr.strip() if e.stderr else "Unknown matugen error"
      raise MatugenError(f"Matugen failed: {error_msg}")
    except json.JSONDecodeError as e:
      raise MatugenError(f"Invalid JSON output: {e}")

  def parse_palette(self, json_palette: dict) -> Palette:
    try:
      all_colors = {
        key: value["default"]["color"]
        for key, value in json_palette["colors"].items()
      }
      return Palette(**all_colors)
    except KeyError as e:
      raise MatugenError(f"Invalid JSON: missing {e}")

  def get_palette(self, image_path: Path, index: int = 0) -> Palette:
    data = self.execute_matugen(image_path, index)
    return self.parse_palette(data)
