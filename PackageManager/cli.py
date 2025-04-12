import click
from .Inspector import KroozInspector
from .Admin import AdminCommands , InvalidateAdmin
from .Manager import GetPossibleDownloads , KroozDownload ,SpitCode
from dotenv import load_dotenv

load_dotenv()

@click.group()
def cli():
  pass

@click.command()
@click.option('--ext', required=False, help="File extension to search for")

def search(ext):
  Packages = KroozInspector()
  data = Packages.GetFilesInfoAsArray()
  if ext:
    for packs in data:
      if str(packs.name).endswith(f".{ext}"):
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
def push(name: str):
  command = AdminCommands()
  isAdmin = InvalidateAdmin()
  if isAdmin:
    command.Push(name)
  else:
    print("You Are Not The Admin Buddy")

@click.command()
@click.option('--name', required=True, help="Remove files from Registry")
def remove(name :str):
  command = AdminCommands()
  command.Delete(name)



cli.add_command(search)
cli.add_command(cat)
cli.add_command(get)
cli.add_command(push)
cli.add_command(remove)

def main():
  cli()
