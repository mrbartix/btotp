

# btotp
An authenticator program written in python.\
Future plans:\
## How it works
btotp takes your TOTP secret base32 strings and encodes them, if you don't know the password (btotp doesn't save your password anywhere) you won't get your codes. 
# Read before using
If you want to configure this app, touch **ONLY** the `BasicInformation` section in `config.toml`.\ 
Do not mess with `presets.toml`, or other sections of `config.toml`. **Do not delete any files and do not change the code**
Config explanation:
```toml
[BasicInformation]
accountName = "mrbartix" #your username, you can change it here
appearance = "system" # theme of the window, valid options: black, white or system
defaultColor = "blue" # default color of widgets, valid options: green, blue, dark-blue
```
## Importing your config
If you want to import your old config.toml (eg. from an old device), just delete the `config.toml` file that you don't want to use and move in your imported `config.toml` file, do not change the name of the config you want to use.
# Installation
To install this program, first check if you have python installed (you have to have python)\
**If you are on windows, make sure that you installed python correctly (tcl and tk have to be installed, also would be nice if python was installed globally and added to PATH).**\
When you are sure that you have installed python then you can head over to releases and get the correct installation script. btotp installer supports:
 - Windows
 - Arch based Linux distros
 - Debian based Linux distros
 - Fedora (red hat) based Linux distros
Run the script with `python path_to_the_script`. If you are on Windows, and installed python without adding it to path, replace `python` with the path to `python.exe`\
On windows the shortcut creation script may have an error leaving you hanging on CMD, just do `CTRL+C`. The error should not be fatal and the shortcuts should still work.

# Manual installation
If you don't trust the installation scripts (or your system is not supported) you can install manually.
## Dependencies
Before installation make sure that you have **Tcl**, **Tk** and the **Times New Roman** font installed.\
**Debian based:**
```bash
sudo apt install python3-tk python3-venv tk tcl ttf-mscorefonts-installer
```
**Arch based (Pacman)**
```bash
sudo pacman -Syu tk tcl
yay -S ttf-ms-fonts
```
(you can also use paru or pamac instead of yay **(use your favourite AUR helper)**)\
**Fedora**
```bash
sudo dnf install python3-tkinter tk tcl curl cabextract xorg-x11-font-utils fontconfig mscore-fonts
```
**Windows**\
When installing python check the **"Use admin privileges when installing py.exe"** and **"Add python.exe to PATH"** options. After that select **"Customize installation"**. Make sure that all boxes on **"Optional Features"** are checked. Press **"Next"**. Make sure that all boxes are checked here too. Press Install.\
**macOS**
```bash
brew install python-tk tcl-tk fontconfig
# you also may need to link tcl/tk
brew link tcl-tk --force
```
## Installation
1. Open the terminal/cmd
2. Make sure that you have **python, [git](https://git-scm.com/)) and the dependencies installed**. Install it if you don't have it.
3. Run:
```bash
git clone https://github.com/mrbartix/btotp.git
cd btotp
```
**Linux or Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
python3 exec.py
```
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd src
python exec.py
```
If you want to exit the venv, use the `deactivate` command.
