# btotp
An authenticator program written in python.\
Future plans:\
installation script
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
# Installation
First, download the source code, using `git clone https://github.com/mrbartix/btotp.git`
1. Open the terminal/cmd
2. Make sure that you have python installed. Install it if you don't have it.
3. Navigate to the directory which the unzipped source code is (using the terminal), and go to the main directory of this script (it's called auth)
4. Inside auth run: 

**Linux or Mac:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
python exec.py
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
