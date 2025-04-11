import os
from dotenv import load_dotenv
import base64
import requests

load_dotenv()
GIT_TOKEN = os.getenv("GIT_TOKN")
REPO_BASE_URL = os.getenv("REPO_BASE_URL")

def Push(name :str , commit : str) -> None:
  current = os.getcwd()
  path = os.path.join(current ,name)
  with open(path, "rb") as file:
    content = file.read()
    encoded_content = base64.b64encode(content).decode()

    url = f"{REPO_BASE_URL}{name}"

    headers = {
        "Authorization": f"token {GIT_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    data = {
        "message": commit,
        "content": encoded_content,
        "branch": "main",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data["sha"] = response.json()["sha"]

    response = requests.put(url, json=data, headers=headers)

    if response.status_code in [200, 201]:
        print("✅ File uploaded successfully!")
    else:
        print("❌ Failed to upload.")


def Delete(name: str, commit: str = "Deleting file") -> None:
  url = f"{REPO_BASE_URL}{name}"

  headers = {
      "Authorization": f"token {GIT_TOKEN}",
      "Accept": "application/vnd.github+json",
  }

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
      sha = response.json().get("sha")

      data = {
          "message": commit,
          "sha": sha,
          "branch": "main",
      }

      delete_response = requests.delete(url, headers=headers, json=data)

      if delete_response.status_code == 200:
          print(f"✅ Deleted '{name}' from repo.")
      else:
          print(f"❌ Failed to delete '{name}'. Status: {delete_response.status_code}\n{delete_response.text}")

  else:
      print(f"❌ File '{name}' not found. Status: {response.status_code}")



def FilesInfoAsArray():
  Content = []
  path  = REPO_BASE_URL
  req = requests.get(path)
  for file in req.json():
      if str(file['name']).startswith(".gitignore"):
          continue
      elif str(file['name']).endswith(".json"):
          continue

      else:
          Content.append(f"{file['name']}")

  return Content
