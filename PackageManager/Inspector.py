import requests
from dataclasses import dataclass
from PackageManager.env import GetEnvMeta

def makeString(string:str):
  return string.strip().lower()


@dataclass
class FileInfo:
    name: str
    type: str
    download_url : str
    size : int = 0

class KroozInspector:
  def __init__(self):
    self.Content: list[FileInfo] = []
    self.URL = f"{GetEnvMeta().REPO_BASE_URL }/"

  def GetFilesInfoAsArray(self) -> list:


    req = requests.get(self.URL)
    for file in req.json():
      info = FileInfo(file["name"], file["type"], file["download_url"], file["size"])
      if str(info.name).startswith("."):
        continue
      if (info.size > 0):
        self.Content.append(info)

    return self.Content

  def GetPackageNames(self) -> list:
    Packages = []
    Contents = self.GetFilesInfoAsArray()
    for info in Contents:
      Packages.append(info.name)

    return Packages

  def GetPackageExt(self) -> dict:
    Packages = {}
    Contents = self.GetFilesInfoAsArray()
    for info in Contents:
      name , ext = str(info.name).split(".")
      Packages[ext] = (name)

    return Packages


  def GetDetails() -> list[FileInfo]:
    Contents : list[FileInfo] = []
    req = requests.get(GetEnvMeta().REPO_BASE_URL)
    for file in req.json():
      info = FileInfo(file["name"], file["type"], file["download_url"], file["size"])
      if str(info.name).startswith("."):
        continue
      if (info.size > 0):
        Contents.append(info)

    return Contents

  def MatchCase(self , name:str) -> str:
    data = self.GetFilesInfoAsArray()
    for files in data:
      if makeString(name) in makeString(files.name):
        return files.download_url

    return ""
