import mimetypes
from pathlib import Path
import subprocess

from paletted.exceptions import FFmpegError, FileFormatError


def get_media_type(file_path: Path) -> str:
  if not mimetypes.inited:
    mimetypes.init()
  mimetypes.add_type("video/x-matroska", ".mkv")

  mime, _ = mimetypes.guess_type(file_path)
  
  if not mime:
    raise FileFormatError(f"Could not determine MIME type for: {file_path.name}")

  if mime.startswith("image/"):
    return "image"
  if mime.startswith("video/"):
    return "video"

  raise FileFormatError(f"Unsupported MIME type: {mime}")


def extract_frame(video_path: Path, image_path: Path, timestamp: str = "00:00:01") -> Path:
  try:
    subprocess.run(
      [
        "ffmpeg", "-ss", timestamp, "-i", str(video_path),
        "-frames:v", "1", "-q:v", "2", "-update", "1", "-y",
        str(image_path)
      ],
      capture_output=True, 
      check=True
    )
    return image_path
  except subprocess.CalledProcessError as e:
    raise FFmpegError(f"Failed to extract frame from video: {e.stderr.decode()}")