from dataclasses import dataclass
import os

@dataclass
class EnvPaths:
  PACKAGE_BASE_URL : str
  PACKAGE_MAIN_URL : str
  GIT_TOKN : str
  REPO_BASE_URL : str
  ADMIN: str
  ADMIN_EMAIL : str


def GetEnvMeta() -> list[EnvPaths]:
  Base = os.getenv("PACKAGE_BASE_URL")
  Main = os.getenv("PACKAGE_MAIN_URL")
  Token = os.getenv("GIT_TOKN")
  Repo = os.getenv("REPO_BASE_URL")
  Admin = os.getenv("ADMIN")
  AdminEmail = os.getenv("ADMIN_EMAIL")

  Info = EnvPaths(Base , Main , Token, Repo ,Admin, AdminEmail)

  return Info

