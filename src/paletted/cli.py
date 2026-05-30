import sys

import typer
from typing_extensions import Annotated
from pathlib import Path

from .paletted import Paletted


class SafeTyper(typer.Typer):
  def __call__(self, *args, **kwargs):
    try:
      return super().__call__(*args, **kwargs)
    except Exception as e:
      typer.secho(str(e), err=True)
      sys.exit(1)

app = SafeTyper(help="Utility for auto generate themes", no_args_is_help=True)

@app.command()
def apply(
  wallpaper_path: Annotated[
    Path, 
    typer.Argument(help="Path to wallpapers", exists=True)
  ],

  config_dir: Annotated[
    Path | None, 
    typer.Option(help="Path to custom config dir. Must contain config.toml")
  ] = None,

  source_index: Annotated[
    int, 
    typer.Option(help="Index of the source color for palette generation (0-3)")
  ] = 0
):
  paletted = Paletted(config_dir)
  paletted.apply_theme(wallpaper_path, source_index)

  typer.secho(f"Theme applied from {wallpaper_path} (index: {source_index})")

@app.command()
def restore(
  config_dir: Annotated[
    Path | None, 
    typer.Option(help="Path to custom config dir. Must contain config.toml")
  ] = None,
): 
  paletted = Paletted(config_dir)
  paletted.restore_wallpaper()

  typer.secho(f"Wallpaper restored")