from pathlib import Path
import shlex
import subprocess

from paletted.exceptions import ConfigError
from .schemas import BackendModel, NotificationModel

class Executer:
  @staticmethod
  def apply_wallpaper(backend: list[BackendModel], wallpaper_path: Path, target_type: str) -> None:
    exec_raw = next((back.exec_line for back in backend if back.type == target_type), None)

    if not exec_raw:
      raise ConfigError(f"Backend config for {target_type} not found")

    if "%wallpaper_path%" not in exec_raw:
      raise ConfigError(f"Incorrect backend config for {target_type}. Must contain %wallpaper_path% placeholder")

    cmd_str = exec_raw.replace("%wallpaper_path%", str(wallpaper_path))
    cmd_list = shlex.split(cmd_str)
    
    Executer.run_hook(cmd_list)

  @staticmethod
  def send_notification(notify: NotificationModel) -> None:
    if not notify.enable: return
    
    cmd_list = ["notify-send", "-a", "Palleted", notify.summary, notify.text]  
    Executer.run_hook(cmd_list)


  @staticmethod
  def run_hook(cmd: list[str]) -> subprocess.Popen:
    process = subprocess.Popen(
      cmd, 
      stdout=subprocess.DEVNULL, 
      stderr=subprocess.DEVNULL,
      start_new_session=True
    )
    
    return process
  