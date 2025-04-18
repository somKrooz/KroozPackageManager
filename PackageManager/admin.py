import os
import base64
import subprocess
import requests
from PackageManager.env import GetEnvMeta

def GetFilePath(name:str) -> str:
  current = os.getcwd()
  return os.path.join(current ,name)


def InvalidateAdmin() -> bool:
    try:
        UserEmail = subprocess.check_output(["git", "config", "user.email"], text=True).strip()
        if UserEmail == GetEnvMeta().ADMIN_EMAIL.strip():
            return True

    except FileNotFoundError:
        return False
    except Exception as e:
        return False

    return False

class AdminCommands:
  def __init__(self):
    pass

  def Push(self, Name:str , RemoteName:str = None) -> None:
    file = GetFilePath(Name)
    try:
      with open(file, "rb") as file:
        content = file.read()
        encoded_content = base64.b64encode(content).decode()

      upload_name = RemoteName if RemoteName else Name
      url = f"{GetEnvMeta().REPO_BASE_URL}/{upload_name}"

      Header = {
        "Authorization" : f"token {GetEnvMeta().GIT_TOKN}",
        "Accept": "application/vnd.github+json",
      }

      data = {
        "message": f"{Name}: has Been Pushed To The Registry",
        "content": encoded_content,
        "branch": "main",
      }

      response = requests.get(url, headers=Header)

      print(response)
      if response.status_code == 200:
        data["sha"] = response.json()["sha"]

      elif response.status_code == 404:
        print(f"{Name} does not exist. Creating new file...")

      response = requests.put(url, json=data, headers=Header)

      if response.status_code ==  200:
        print("Successfully Pushed.." , "success")
      else:
        print("Failed To Push.." , "error")

    except FileNotFoundError:
      print("File  not found." , "error")
    except Exception as e:
      print("An error occurred: " , {e})


  def Delete(self , name) -> None:
    try:
      url = GetEnvMeta().REPO_BASE_URL + "/" + name
      Header = {
        "Authorization" : f"token {GetEnvMeta().GIT_TOKN}",
        "Accept": "application/vnd.github+json",
      }

      response = requests.get(url, headers=Header)
      if response.status_code == 200:
        sha = response.json()['sha']
      else:
          print("File Does Not Exist On The Registry")
          return

      data = {
        "message": f"{name}: has Been Removed From The Registry",
        "sha" : sha,
        "branch": "main"
      }

      response = requests.delete(url, headers=Header, json=data)
      if response.status_code == 200:
        print("Sucessfully Removed")
      else:
        print("Failed to Remove")

    except Exception as e:
       print(f"Error {e}")
