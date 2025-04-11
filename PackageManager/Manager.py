import os
import requests
from dotenv import load_dotenv
import subprocess
from .admin import FilesInfoAsArray


load_dotenv()

PACKAGE_BASE_URL = os.getenv("PACKAGE_BASE_URL")
PACKAGE_MAIN_URL = os.getenv("PACKAGE_MAIN_URL")

def make_short(name: str) -> str:
    return name.strip().lower()


def matchFuzz(name:str) -> str:
    input = make_short(name)
    packages = search_query()

    for ext, filename in packages.items():
      if input.__contains__(make_short(filename)):
          return f"{filename}.{ext}"



def get_packages_by_ext(ext: str) -> None:
    packages = FilesInfoAsArray()
    for package in packages:
        if package.endswith(f".{ext}"):
            name, ext = package.rsplit(".", 1)
            print(f"* {name} -> {ext}")


def fuzzy_find(arr: dict, query: str) -> None:
    query_normalized = make_short(query)
    for item in arr.values():
        token = make_short(item)
        if query_normalized in token:
            print(f"{item} has {query}")


def search_query():
    Contents = {}
    packages = FilesInfoAsArray()

    for i in packages:
      parts  = i.split(".")
      if parts != None:
        name, ext = parts
        Contents[ext] = name

    return Contents


def CreateUrl(name: str) -> str:
  PackageName = matchFuzz(name)
  URL = PACKAGE_MAIN_URL + PackageName
  return URL

def Invalidate():
  UserName = subprocess.check_output(["git", "config","user.name"])
  UserEmail = subprocess.check_output(["git", "config","user.email"])

  if UserName == "somkrooz":
      print("You Are Good to Push Files..")
  else:
      print("Only admin Can Push Files..")


def create_download(name: str) -> None:
    try:
        package = matchFuzz(name)
        url = f"{PACKAGE_BASE_URL}/{package}"
        response = requests.get(url)

        with open(package, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {package}...")

    except Exception as e:
        print(f"Error downloading package: {e}")

def HardDownload(name: str) -> None:
  try:
    url = f"{PACKAGE_BASE_URL}/{name}"
    response = requests.get(url)
    with open(name, "wb") as file:
        file.write(response.content)
    print(f"Downloaded {name} ...")

  except Exception as e:
      print(f"Error downloading package: {e}")


def LookForRelations(name:str):
  Content = []
  Packages = FilesInfoAsArray()
  for i in Packages:
     packs = make_short(i)
     if make_short(name) in packs:
        if str(packs).endswith(".h"):
          Content.append(i)
        elif str(packs).endswith(".cpp"):
          Content.append(i)

  return Content


