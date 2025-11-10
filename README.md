
# btotp
An authenticator program written in python.\
Future plans:\
[x] installation script
## How it works
btotp takes your TOTP secret base32 strings and encodes them, if you dont know the password (btotp doesn't save your password anywhere) you won't get your codes. 
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
# Dependencies
Before installation make sure that you have **Tcl**, **Tk** and the **Times New Roman** font installed.
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
When installing python check the **"Use admin privileges when installing py.exe"** and **"Add python.exe to PATH"** options. After that select **"Customize installation"**. Make sure that all boxes on **"Optional Features"** are checked. Press **"Next"**. Make sure that all boxes are checked here too. Press Install.
**macOS**
```bash
brew install python-tk tcl-tk fontconfig
# you also may need to link tcl/tk
brew link tcl-tk --force
```
# Installation
1. Open the terminal/cmd
2. Make sure that you have **python, [git](https://git-scm.com/)) and the dependencies installed**. Install it if you don't have it.
3. Run:
`git clone https://github.com/mrbartix/btotp.git` 
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
