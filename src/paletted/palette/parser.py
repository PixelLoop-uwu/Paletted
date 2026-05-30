from collections.abc import Sequence
import colorsys
import re

from paletted.exceptions import ColorNameError, ModifierArgError, ModifierNameError
from .schemas import Palette


class ColorParser:
  """Parses color placeholders and applies chained modifiers."""

  _MODIFIER_RE = re.compile(
    r"^([a-z]+)(?:\(([^)]*)\))?$"
  )

  _SPLIT_RE = re.compile(
    r"(?<!\d)\.(?!\d)"
  )

  def __init__(self, palette: Palette):
    self.palette = palette.model_dump()

    self.modifiers = {
      "alpha": self._alpha,
      "dark": self._dark,
      "light": self._light,
      "sat": self._sat,
      "rgb": self._rgb,
      "strip": self._strip,
    }

  def parse_placeholder(self, placeholder: str) -> str:
    """
    Example:
      {primary.dark(1.2).alpha(0.5)}
    """
    clean = placeholder.strip("{} ")
    color_name, *mods = self._SPLIT_RE.split(clean)

    if color_name not in self.palette:
      raise ColorNameError(f"Color '{color_name}' not found.")

    color = self.palette[color_name]

    for mod in mods:
      color = self._apply_modifier(color, mod)

    return color

  def _apply_modifier(self, color: str, modifier: str) -> str:
    match = self._MODIFIER_RE.match(modifier)

    if not match:
      raise ModifierNameError(f"Modifier error: {modifier}")

    name, arg = match.groups()

    value = (
      float(arg)
      if arg and arg.strip()
      else 1.0
    )

    if not (0 <= value <= 5):
      raise ModifierArgError(
        f"Argument {name}({value}) out of range [0, 5]"
      )

    handler = self.modifiers.get(name)

    if handler is None:
      raise ModifierNameError(f"Method {name} is not supported")

    return handler(color, value)

  # --------------------------------------------------------------------------
  # Utilities
  # --------------------------------------------------------------------------

  def _split_hex(self, hex_str: str) -> tuple[str, int | None]:
    clean = hex_str.lstrip("#")
    if len(clean) == 8:
      return "#" + clean[:6], int(clean[6:], 16)
    return "#" + clean, None

  def _hex_to_rgb(self, hex_str: str) -> list[int]:
    clean = hex_str.lstrip("#")
    return [int(clean[i:i + 2], 16) for i in (0, 2, 4)]

  def _rgb_to_hex(self, rgb: Sequence[float], alpha: float | int | None = None) -> str:
    rgb = [max(0, min(255, int(c))) for c in rgb]
    hex_str = "{:02x}{:02x}{:02x}".format(*rgb)
    if alpha is not None:
      hex_str += "{:02x}".format(max(0, min(255, int(alpha))))
    return "#" + hex_str

  def _parse(self, hex_val: str) -> tuple[list[int], int | None]:
    hex_rgb, alpha = self._split_hex(hex_val)
    return self._hex_to_rgb(hex_rgb), alpha

  # --------------------------------------------------------------------------
  # Modifiers
  # --------------------------------------------------------------------------

  def _alpha(self, hex_val: str, factor: float) -> str:
    rgb, _ = self._parse(hex_val)
    return self._rgb_to_hex(rgb, alpha=factor * 255)

  def _dark(self, hex_val: str, factor: float) -> str:
    rgb, alpha = self._parse(hex_val)
    
    r, g, b = [c / 255 for c in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0.0, min(1.0, l / factor))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    
    return self._rgb_to_hex([r * 255, g * 255, b * 255], alpha)

  def _light(self, hex_val: str, factor: float) -> str:
    rgb, alpha = self._parse(hex_val)
    
    r, g, b = [c / 255 for c in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    if factor != 1.0:
        base_lighten = 0.2 * factor
        l = l + (1.0 - l) * base_lighten
        l = max(0.0, min(1.0, l))
        
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return self._rgb_to_hex([r * 255, g * 255, b * 255], alpha)

  def _sat(self, hex_val: str, factor: float) -> str:
    rgb, alpha = self._parse(hex_val)
    r, g, b = [c / 255 for c in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = max(0.0, min(1.0, s * factor))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return self._rgb_to_hex([r * 255, g * 255, b * 255], alpha)

  def _rgb(self, hex_val: str, factor: float) -> str:
    rgb, alpha = self._parse(hex_val)
    if alpha is not None:
      a = round(alpha / 255, 2)
      a = int(a) if a.is_integer() else a
      return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {a})"
    return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"

  def _strip(self, hex_val: str, factor: float) -> str:
    return hex_val.lstrip("#")