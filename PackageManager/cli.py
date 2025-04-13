import click
from PackageManager.Inspector import KroozInspector
from PackageManager.Admin import AdminCommands , InvalidateAdmin
from PackageManager.Manager import GetPossibleDownloads , KroozDownload ,SpitCode
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
print(env_path)

@click.group()
def cli():
  pass

@click.command()
@click.option('--name', required=False, help="File extension to search for")
def search(name):
  Packages = KroozInspector()
  data = Packages.GetFilesInfoAsArray()
  if name:
    for packs in data:
      if str(packs.name).endswith(f".{name}"):
        print(f"➤ {packs.name} -> {packs.type}")
  else:
    for pack in data:
      print(f"➤ {pack.name} -> {pack.type}")

@click.command()
@click.option('--name', required=True, help="Cat The File in Terminal")
def cat(name:str):
  Packages = KroozInspector()
  data = Packages.MatchCase(name)
  if(data != ""):
    SpitCode(data)

@click.command()
@click.option('--name', required=True, help="Download The File")
@click.option('--force', is_flag=True , help="Force it to Download the same name Headers")
def get(name: str , force: bool):
  if not force:
    packs = GetPossibleDownloads(name , False)
    KroozDownload(packs)
  else:
    packs = GetPossibleDownloads(name , True)
    KroozDownload(packs)

@click.command()
@click.option('--name', required=True, help="Push files on Registry")
@click.option('--file', default=None, help="Push files on Registry")
def push(name: str , file:str):
  command = AdminCommands()
  isAdmin = InvalidateAdmin()
  if isAdmin:
    command.Push(name, RemoteName= file)
    print(f"Pushed {name} Successfully...")
  else:
    print("You Are Not The Admin Buddy")


@click.command()
@click.option('--name', required=True, help="Remove files from Registry")
def remove(name :str):
  command = AdminCommands()
  isAdmin = InvalidateAdmin()
  if isAdmin:
    command.Delete(name)
    print(f"Removed {name} Successfully...")
  else:
    print("You Are Not The Admin Buddy")

cli.add_command(search)
cli.add_command(cat)
cli.add_command(get)
cli.add_command(push)
cli.add_command(remove)

def main():
  cli()
