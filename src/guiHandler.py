# btotp - Simple TOTP Authenticator
# Copyright (C) 2025 mrbartix [bartixalt@gmail.com]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import customtkinter as ctk
import time, os, toml

path = f"{os.path.dirname(os.path.abspath(__file__))}/../resources/config.toml"
if not os.path.isfile(path):
 ctk.set_appearance_mode("system")
 ctk.set_default_color_theme("blue")
else:
 config = toml.load(path)
 basic = config.get("BasicInformation", {})
 appearance = basic.get("appearance", "system")
 color = basic.get("defaultColor", "blue")
 ctk.set_appearance_mode(appearance)
 ctk.set_default_color_theme(color)

class AuthField(ctk.CTkFrame):
 """
 AuthField is a custom widget written in customTkniter (only)
 It's meant to be used in a dictionary
 If you need one of these, dont use a dictionary i guess?
 I've designed it to be used in an app with a button
 Args:
  parent (widget): Parent widget, eg. root
  editcmd (function): Function which will get executed when the user presses the edit button
  deletecmd (function): Function which will get executed when the user preses the delete button
  cliboardcmd (function): Function which will put the TOTP code in the user's clipboard
  root (CTk): Main window
  key (int): Unique identifier for the field
 """
 def __init__(self, parent, editcmd=None, deletecmd=None, root=None, key=None):
  super().__init__(parent, width=410, height=150, corner_radius=5, border_width=2)
  self.pack_propagate(False)
  self.key = key

  self.codelabel = ctk.CTkLabel(self, text="lorem ipsum", font=("Times New Roman", 18), anchor="w")
  self.codelabel.place(x=5, y=5)

  self.code = ctk.CTkEntry(self, font=("Times New Roman", 52), width=170)
  self.code.insert(0,"------")
  self.code.configure(state="readonly")
  self.code.place(x=6, y=80)

  self.timer = ctk.CTkLabel(self, text="🕐tts", font=("Times New Roman", 35), anchor="w")
  self.timer.place(x=230, y=52)

  self.edit = ctk.CTkButton(self, command=editcmd, text="🖉", font=("Times New Roman", 25), width=40, height=30)
  self.edit.place(x=360, y=5)

  self.delete = ctk.CTkButton(self, command=deletecmd, text="🗑", font=("Times New Roman", 30), width=40, height=30, fg_color="red")
  self.delete.place(x=360, y=102)

  self.copy = ctk.CTkButton(self, command=lambda: [root.clipboard_clear(), root.clipboard_append(str(self.code.get()))], text="📄", font=("Times New Roman", 30), width=40, height=30, fg_color="green")
  self.copy.place(x=360, y=50)

  self.timeUptd()

 def timeUptd(self):
  """
  This function is not to be used
  """
  self.timer.configure(text=f"🕐{int(round(30 - (time.time() % 30), 0))}s")
  self.after(1000, self.timeUptd)

 def updateTitle(self, new_title):
  """
  This function is not to be used
  """
  self.codelabel.configure(text=new_title)

class EditPopUp(ctk.CTkToplevel):
 """
 A Pop up which lets the user edit the title of their TOTP code.
 Args:
  yescmd=function: when user confirms the edit, a function has to be executed
 """
 def __init__(self, parent, titleVar, yescmd=None):
  super().__init__(parent)
  self.geometry("270x120")
  self.title("Edit title")
  self.resizable(False,False)

  self.Label = ctk.CTkLabel(self, text="Enter new title:")
  self.Label.place(x=80,y=5)

  self.entry = ctk.CTkEntry(self, width=200, textvariable=titleVar)
  self.entry.place(x=30,y=35)

  self.yes = ctk.CTkButton(self, text="Save", width=80, fg_color="green", command=yescmd)
  self.yes.place(x=30, y=75)

  self.cancel = ctk.CTkButton(self, text="Cancel", width=80, fg_color="red", command=lambda: self.destroy())
  self.cancel.place(x=140, y=75)

class YesNoPopUpWindow(ctk.CTkToplevel):
 """
 Used for creating a yes/no pop up window
 Args:
  title (str): Title of the window
  labelTxt (str): Text of the label that is in the window
  yesAction (function): Function that is going to be executed when user presses "Ok"
 """
 def __init__(self, parent, title=str, labelTxt=str, yesAction=None):
  super().__init__(parent)
  self.geometry("250x90")
  self.title(title)
  self.resizable(False,False)
  self.transient(parent)
  self.focus_force()
  self.Label = ctk.CTkLabel(self, text=labelTxt)
  self.Label.place(x=85,y=5)
  self.yes = ctk.CTkButton(self, text="Yes", width=80, fg_color="green", command=lambda: [yesAction(), self.destroy()])
  self.yes.place(x=30, y=40)
  self.cancel = ctk.CTkButton(self, text="No", width=80, fg_color="red", command=lambda: self.destroy())
  self.cancel.place(x=140, y=40)

class AddField(ctk.CTkFrame):
 """
 Used for creating a button which is meant to add auth widgets
 Args:
  parent (widget): The widget which is the parent of this button
  action (function): Function that is going to be executed after pressing this button
 """
 def __init__(self, parent, action=None):
  super().__init__(parent, width=410, height=150)
  self.pack_propagate(False)
  self.button = ctk.CTkButton(self, text="+", font=("Times New Roman", 40), command=action)
  self.button.pack(fill="both", expand=True)

class RegisterWindow(ctk.CTkToplevel):
 """A window which lets the user register
 Args:
  parent (widget): parent of the window, eg. root
  passwordVar (ctk.StringVar()): a place which will store the password after the registration is complete
  usernameVar (ctk.StringVar()): a place which will store the username after the registration is complete
  registerCmd (function): function that will get executed when the registration is finished
 """
 def __init__(self, parent, passwordVar, usernameVar, registerCmd):
  super().__init__(parent)
  self.title("Registration")
  self.resizable(0,0)
  self.geometry("350x250")
  self.grab_set()
  self.transient(parent)
  self.focus_force()
  self.welcome = ctk.CTkLabel(self, text="Welcome to the registration of mAuth!", font=("Times New Roman", 18))
  self.welcome.place(x=35, y=5)
  self.idk = ctk.CTkLabel(self, text="Set your username and password", font=("Times New Roman", 18))
  self.idk.place(x=60, y=25)
  self.warning = ctk.CTkLabel(self, text="WARNING: If you forget your password, \n you cannot recover it.", font=("Times New Roman", 18), text_color="red")
  self.warning.place(x=25, y=49)
  self.utxt = ctk.CTkLabel(self, text="username:", font=("Times New Roman", 18))
  self.utxt.place(x=20, y=100)
  self.username = ctk.CTkEntry(self, textvariable=usernameVar)
  self.username.place(x=100, y=100)
  self.ptxt = ctk.CTkLabel(self, text="password:", font=("Times New Roman", 18))
  self.ptxt.place(x=20, y=140)
  self.password = ctk.CTkEntry(self, textvariable=passwordVar, show = '*')
  self.password.place(x=100, y=140)
  self.submit = ctk.CTkButton(self, text="submit", width=80, fg_color="green", command=lambda: [registerCmd()])
  self.submit.place(x=80, y=200)
  self.cancel = ctk.CTkButton(self, text="cancel", width=80, fg_color="red", command=lambda: [self.destroy(), parent.destroy()])
  self.cancel.place(x=200, y=200)

class RegisterTOTPWindow(ctk.CTkToplevel):
 """A window which lets the user register
 Args:
  parent (widget): parent of the window, eg. root
  secretVar (ctk.StringVar()): a place which will store the secret after the field registration is complete
  titleVar (ctk.StringVar()): a place which will store the title after the field registration is complete
  addCmd (function): function that will get executed when the field registration is finished
 """
 def __init__(self, parent, secretVar, titleVar, addCmd):
  super().__init__(parent)
  self.transient(parent)
  self.focus_force()
  self.title("Add a TOTP field")
  self.resizable(0,0)
  self.geometry("350x260")
  self.transient(parent)
  self.focus_force()
  self.welcome = ctk.CTkLabel(self, text="Register a field", font=("Times New Roman", 18))
  self.welcome.place(x=120, y=5)
  self.idk = ctk.CTkLabel(self, text="Enter the secret string \n provided by the app, and your title", font=("Times New Roman", 18))
  self.idk.place(x=50, y=25)
  self.ttxt = ctk.CTkLabel(self, text="title:", font=("Times New Roman", 18))
  self.ttxt.place(x=60, y=100)
  self.tEntry = ctk.CTkEntry(self, textvariable=titleVar)
  self.tEntry.place(x=100, y=100)
  self.stxt = ctk.CTkLabel(self, text="secret:", font=("Times New Roman", 18))
  self.stxt.place(x=50, y=140)
  self.secret = ctk.CTkEntry(self, textvariable=secretVar, show = '*')
  self.secret.place(x=100, y=140)
  self.output = ctk.CTkLabel(self, text="", font=("Times New Roman", 18), text_color="red")
  self.output.place(x=20, y=180)
  self.submit = ctk.CTkButton(self, text="submit", width=80, fg_color="green", command=addCmd)
  self.submit.place(x=80, y=220)
  self.cancel = ctk.CTkButton(self, text="cancel", width=80, fg_color="red", command=lambda: self.destroy())
  self.cancel.place(x=200, y=220)

class LoginPopUp(ctk.CTkToplevel):
 """A window which lets the user login
 Args:
  parent (widget): parent of the window, eg. root
  passwordVar (ctk.StringVar()): a place which will store the password after the login is complete
  usernameVar (ctk.StringVar()): a place which will store the username after the login is complete
  loginCmd (function): function that will get executed when the login process is finished
  deleteDataCmd (function): if the user forgets their password, and want to delete their data, this command will be executed
 """
 def __init__(self, parent, usernameVar, passwordVar, loginCmd, deleteDataCmd):
  super().__init__(parent)
  self.grab_set()
  self.transient(parent)
  self.focus_force()
  self.title("Login")
  self.resizable(0,0)
  self.geometry("350x250")
  self.grab_set()
  self.transient(parent)
  self.focus_force()
  self.deleteData = ctk.CTkButton(self, text="I forgot my password! - Delete all data [this will delete it]", width=80, text_color="red", fg_color="transparent", command=lambda: [deleteDataCmd(), self.destroy(), parent.destroy()])
  self.deleteData.place(x=0, y=0)
  self.welcome = ctk.CTkLabel(self, text="Welcome back! Login to begin", font=("Times New Roman", 18))
  self.welcome.place(x=60, y=28)
  self.idk = ctk.CTkLabel(self, text="Enter your username and the password", font=("Times New Roman", 18))
  self.idk.place(x=30, y=50)
  self.utxt = ctk.CTkLabel(self, text="username:", font=("Times New Roman", 18))
  self.utxt.place(x=20, y=85)
  self.uEntry = ctk.CTkEntry(self, textvariable=usernameVar)
  self.uEntry.place(x=100, y=85)
  self.ptxt = ctk.CTkLabel(self, text="password:", font=("Times New Roman", 18))
  self.ptxt.place(x=20, y=125)
  self.password = ctk.CTkEntry(self, textvariable=passwordVar, show = '*')
  self.password.place(x=100, y=125)
  self.output = ctk.CTkLabel(self, text="", font=("Times New Roman", 18), text_color="red")
  self.output.place(x=20, y=160)
  self.submit = ctk.CTkButton(self, text="login", width=80, fg_color="green", command=lambda: loginCmd())
  self.submit.place(x=75, y=200)
  self.cancel = ctk.CTkButton(self, text="exit", width=80, fg_color="red", command=lambda: [self.destroy(), parent.destroy()])
  self.cancel.place(x=195, y=200)
