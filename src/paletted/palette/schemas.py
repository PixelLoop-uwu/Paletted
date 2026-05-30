from pydantic import BaseModel, ConfigDict


class Palette(BaseModel):
  model_config = ConfigDict(extra='ignore')

  # --- PRIMARY (Accent / Brand Color) ---
  primary: str
  """Main interface color used for primary buttons, active states, and important UI elements."""

  on_primary: str
  """Text and icons displayed on top of the primary color."""

  primary_container: str
  """Container background for medium-emphasis elements such as FABs or highlighted cards."""

  on_primary_container: str
  """Text and icons displayed on the primary container background."""

  # --- SECONDARY (Secondary Accent Color) ---
  secondary: str
  """Less prominent accent color used for chips, filters, toggles, and supporting UI elements."""

  on_secondary: str
  """Text and icons displayed on top of the secondary color."""

  secondary_container: str
  """Soft background for secondary content blocks or subtle highlights."""

  on_secondary_container: str
  """Text and icons displayed on the secondary container background."""

  # --- TERTIARY (Additional Accent Color) ---
  tertiary: str
  """Additional contrasting accent color used for distinct interactive elements."""

  on_tertiary: str
  """Text and icons displayed on top of the tertiary color."""

  tertiary_container: str
  """Soft background for elements requiring additional emphasis without being overly strong."""

  on_tertiary_container: str
  """Text and icons displayed on the tertiary container background."""

  # --- SURFACE & BACKGROUND ---
  background: str
  """Root application background color."""

  on_background: str
  """Primary text color displayed on the application background."""

  surface: str
  """Surface color used for cards, menus, dialogs, sheets, and other components."""

  on_surface: str
  """Text and icons displayed on surface elements."""

  surface_variant: str
  """Alternative surface shade used for elements such as search bars or nested surfaces."""

  on_surface_variant: str
  """Secondary text and icons displayed on surface variants."""

  # --- OUTLINES & BORDERS ---
  outline: str
  """High-contrast borders and dividers."""

  outline_variant: str
  """Low-contrast decorative borders and subtle separators."""

  # --- ERROR COLORS ---
  error: str
  """Color used for errors, destructive actions, and critical warnings."""

  on_error: str
  """Text and icons displayed on top of the error color."""

  error_container: str
  """Soft background for error messages and warning containers."""

  on_error_container: str
  """Text and icons displayed on the error container background."""

  # --- INVERSE COLORS ---
  inverse_surface: str
  """Inverted surface color used for snackbars or temporary overlays."""

  inverse_on_surface: str
  """Text and icons displayed on inverted surfaces."""

  inverse_primary: str
  """Primary accent color used inside inverted UI elements."""