import urllib.request, zipfile, os, tempfile, subprocess, sys

default_download_dir = ""
sudo = ""

def get_data():
 global default_download_dir, sudo
 d = input("\nWhere do you want to install btotp to?\nDeafult directory: /home/username/bin/btotp\nYou shouldn't input path/btotp, since directory 'btotp-main' will get created\nIf the directory doesn't exit, it will be created\nInput: ")
 if d:
  home = os.path.expanduser("~")
  d = d.replace("~", home)
  default_download_dir = d
 else: default_download_dir = os.path.join(os.path.expanduser("~"), "bin")
 os.makedirs(default_download_dir, exist_ok=True)
 s = input("What sudo-like program do you use? [default sudo] eg. sudo, doas: ")
 if not s:
  sudo = "sudo"
 else: sudo = s

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
 os.remove(f"{default_download_dir}/btotp-main/setups")
 print("Download done")

def get_dependencies(): # Downloads the dependencies with dnf
 print("\n[1/4] Checking for needed packages...")
 def check_installed(pkg): 
  result = subprocess.run(["rpm", "-q", pkg],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  return result.returncode == 0
 if not check_installed("tcl") or not check_installed("tk") or not check_installed("python3-tkinter") or not check_installed("cabextract") or not check_installed("xorg-x11-font-utils") or not check_installed("mscore-fonts") or not check_installed("fontconfig"):
  print("[2/4] Some dependency is not installed. Installing...\n")
  print("[3/4] Updating the system; running dnf upgrade...")
  subprocess.run([sudo,"dnf","upgrade"], check=True)
  print("[4/4] Installing python3-tkinter tk tcl curl cabextract xorg-x11-font-utils fontconfig mscore-fonts...")
  subprocess.run([sudo,"dnf","install","python3-tkinter","tk","tcl","cabextract","xorg-x11-font-utils","fontconfig","mscore-fonts"], check=True)
 else: print("[2/4] Skipped\n[3/4] Skipped\n[4/4] APT dependencies already satisfied")
 print("Dependencies Satisfied")

def setup_venv(): # sets up the venv, and installs pip dependencies.
 print("\nVenv setup")
 print("[1/2] Setting up the venv")
 subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=f"{default_download_dir}/btotp-main", check=True)
 print("[2/2] Installing pip dependencies")
 subprocess.run([f"{default_download_dir}/btotp-main/venv/bin/pip", "install", "-r", "requirements.txt"], cwd=f"{default_download_dir}/btotp-main", check=True)

def finalize(): # creates a shortcut to exec.py
 i = input("Do you want to set up a shortcut to btotp? [y/n]: ").lower()
 if i == "n":
  return
 print("[1/1] Creating a .desktop file")
 subprocess.run(["touch", "btotp.desktop"], cwd=f"{default_download_dir}/btotp-main", check=True)
 with open(f"{default_download_dir}/btotp-main/btotp.desktop", "w") as f:
  f.write(f"""[Desktop Entry]
  Type=Application
  Name=btotp
  Icon={default_download_dir}/btotp-main/resources/icon.png
  Exec="{default_download_dir}/btotp-main/venv/bin/python {default_download_dir}/btotp-main/src/exec.py"
  Comment=Python TOTP authenticator app
  Terminal=false
  """)
  f.flush()
 ask = input("Do you want to make the shortcut accessible systemwide  [requires sudo] [y/n]: ").lower()
 if ask == "y":
  subprocess.run([sudo, "cp",f"{default_download_dir}/btotp-main/btotp.desktop","/usr/share/applications"])
 else:
  subprocess.run(["cp",f"{default_download_dir}/btotp-main/btotp.desktop",f"{os.path.expanduser("~")}/.local/share/applications"])

def self_delete():
 path = os.path.abspath(sys.argv[0])
 if sys.platform.startswith("win"): 
  subprocess.Popen(["cmd", "/c", f"timeout 2 >nul & del /f /q \"{path}\""], shell=True)
 else: 
  subprocess.Popen(["sh", "-c", f"sleep 2 && rm -f '{path}'"])

if __name__ == "__main__":
 if os.geteuid() == 0:
  print("Do not run as root!")
  exit(1)
 print("btotp installer for Fedora")
 print("Make sure that you really are on a Fedora based system")
 print("By 'Fedora based' I mean that your system has to use dnf")
 q = input("Do you want to continue? [y/n] ").lower()
 if q == "n":
  quit()
 get_data()
 download()
 get_dependencies()
 setup_venv()
 finalize()
 print("\nDone, deleting this script")
 self_delete()
