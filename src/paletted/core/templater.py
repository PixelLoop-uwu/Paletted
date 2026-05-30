from pathlib import Path
import re

from paletted.palette import ColorParser
from .schemas import PackageModel


class Templater:
  def render(self, template_dir: Path, package: PackageModel, parser: ColorParser) -> None:
    template_path = template_dir / package.template
    
    if not template_path.exists():
      raise FileNotFoundError(f"Template not found: {template_path}")

    content = template_path.read_text()
    
    rendered = re.sub(
      r'\{\{\s*(.*?)\s*\}\}', 
      lambda m: str(parser.parse_placeholder(m.group(1))), 
      content
    )

    target_path = Path(package.target).expanduser()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(rendered)