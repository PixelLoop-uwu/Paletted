from pydantic import BaseModel, Field
from pathlib import Path

class PackageModel(BaseModel):
  name: str
  template: str
  target: str
  exec_commands: list[list[str]] = Field(default_factory=list, alias="exec")


class SettingsModel(BaseModel):
  source_image: Path | None = Field(default=None)


class BackendModel(BaseModel):
  type: str
  exec_line: str = Field(..., alias="exec")


class AppliersModel(BaseModel):
  applier: str | None = Field(default=None)


class NotificationModel(BaseModel):
  enable: bool = Field(default=False)
  summary: str = Field(default='')
  text: str = Field(default='')


class Config(BaseModel):
  package: list[PackageModel] = Field(default_factory=list)
  backend: list[BackendModel] = Field(default_factory=list)
  appliers: list[AppliersModel] = Field(default_factory=list)
  settings: SettingsModel = Field(default_factory=SettingsModel)
  notification: NotificationModel = Field(default_factory=NotificationModel)