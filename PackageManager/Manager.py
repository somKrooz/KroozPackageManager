from .env import GetEnvMeta
from .Inspector import KroozInspector
import requests

def makeString(string:str):
  return string.strip().lower()


def GetPossibleDownloads(name:str , force: bool = False) -> list:
  PackageData = KroozInspector.GetDetails()
  HPfile = []
  for files in PackageData:
    if makeString(name) in makeString(files.name):
      HPF = files.name
      HPfile.append(HPF)
      if not force:
        break

  return HPfile

def KroozDownload(HPF: list) -> None:
  try:
    for files in HPF:
      URL = f"{GetEnvMeta().PACKAGE_BASE_URL}/{files}"
      response = requests.get(URL)
      with open(files, "wb") as file:
        file.write(response.content)

  except Exception as e:
    print(f"Error Occured {e}" , "error")


def SpitCode(url:str) -> None:
  req = requests.get(url)
  print(req.text)
