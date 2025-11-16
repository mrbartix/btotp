import urllib.request, zipfile, os, tempfile, subprocess, sys, tempfile

default_download_dir = ""

def get_data():
 global default_download_dir
 n = fr"""{os.path.join(os.environ["LOCALAPPDATA"], "btotp-main")}""" #prevents it from breaking on \
 m = r"path\btotp"
 d = input(f"\nWhere do you want to install btotp to?\nDeafult directory: {n}\nYou shouldn't input {m}, since directory 'btotp-main' will get created\nIf the directory doesn't exit, it will be created\nInput: ")
 if d:
  d = d.replace("\\", "\\\\")
  d = os.path.normpath(d)
  default_download_dir = fr"{d}"
 else: default_download_dir = {os.environ["LOCALAPPDATA"]}
 os.makedirs(default_download_dir, exist_ok=True)

def download(): # Downloads the repository as a zip archive, which skips the need of git and uzips it
 url = "https://github.com/mrbartix/btotp/archive/refs/heads/main.zip"
 temp_dir = os.path.join(tempfile.gettempdir(), "btotp-repo.zip")
 print(f"[1/3] Downloading the repository as zip to {temp_dir}")
 urllib.request.urlretrieve(url, temp_dir)
 with zipfile.ZipFile(temp_dir, 'r') as z:
  print(f"[2/3] Unzipping the downloaded zip file at {default_download_dir}")
  z.extractall(default_download_dir)
 print(f"[3/3] Removing {temp_dir}")
 os.remove(temp_dir)
 os.remove(fr"{default_download_dir}\btotp-main\setups")
 print("Download done")

def setup_venv(): # sets up the venv, and installs pip dependencies.
 print("\nVenv setup")
 print("[1/2] Setting up the venv")
 project = os.path.join(default_download_dir, "btotp-main")
 subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=project, check=True)
 print("[2/2] Installing pip dependencies")
 subprocess.run([fr"{default_download_dir}\btotp-main\venv\Scripts\pip", "install", "-r", "requirements.txt"], cwd=project, check=True)

def finalize(): #creates the shortcut
 i = input("Do you want to set up a shortcut to btotp [start menu and desktop]? [y/n]: ").lower()
 if i == "n":
  return

 print("[1/3] Creating a powershell script, which will create the shortcut")

 script = fr"""
 $python = "{default_download_dir}\btotp-main\venv\Scripts\pythonw.exe"
 $scriptPath = "{default_download_dir}\btotp-main\src\exec.py"
 $icon = "{default_download_dir}\btotp-main\resources\icon.ico"
 $shortcutName = "btotp.lnk"

 $desktop = [Environment]::GetFolderPath("Desktop")
 $startMenu = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"

 $desktopShortcut = Join-Path $desktop $shortcutName
 $startMenuShortcut = Join-Path $startMenu $shortcutName

 $wsh = New-Object -ComObject WScript.Shell

 $s1 = $wsh.CreateShortcut($desktopShortcut)
 $s1.TargetPath = $python
 $s1.Arguments = "`"$scriptPath`""
 $s1.WorkingDirectory = Split-Path $scriptPath
 $s1.IconLocation = $icon
 $s1.Save()

 $s2 = $wsh.CreateShortcut($startMenuShortcut)
 $s2.TargetPath = $python
 $s2.Arguments = "`"$scriptPath`""
 $s2.WorkingDirectory = Split-Path $scriptPath
 $s2.IconLocation = $icon
 $s2.Save()

 Write-Host "[PS1] Shortcuts created."
 """

 temp_script = os.path.join(tempfile.gettempdir(), "btotp_shortcuts.ps1")
 with open(temp_script, "w", encoding="utf-8") as f:
  f.write(script)
  f.flush()

 print("[2/3] Executing the powershell script...")

 ch = input("If you are paranoid about a virus, you can see the script now [I'll print it out]; [y/n]: ").lower()
 if ch == "y":
  print(f"Finee, here you go...\n{script}")

 subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", temp_script], check=True)

 print("[3/3] Cleaning up...")
 os.remove(temp_script)

def self_delete():
 path = os.path.abspath(sys.argv[0])
 if sys.platform.startswith("win"): 
  subprocess.Popen(["cmd", "/c", f"timeout 2 >nul & del /f /q \"{path}\""], shell=True)
 else: 
  subprocess.Popen(["sh", "-c", f"sleep 2 && rm -f '{path}'"])

if __name__ == "__main__":
 print("btotp installer for Windows")
 print("Make sure that you really are on Windows")
 q = input("Do you want to continue? [y/n] ").lower()
 if q == "n":
  quit()
 print("Checking if you have installed python correctl [checking for tk and tcl]...")
 try:
  import tkinter as tk
  root = tk.Tk()
  root.withdraw()
  root.update()
  root.destroy()
  print("Tkinter test passed")
 except:
  print("CRITICAL: Can't continue; tkinter wasnt imported correctly!")
  print("Reinstall python and make sure that you have tcl and tk installed")
  quit()
 get_data()
 download()
 setup_venv()
 finalize()
 print("\nDone, deleting this script")
 self_delete()
