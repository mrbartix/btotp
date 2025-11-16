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
from configHandler import CriticalConfigError, ConfigHandler, SecretHandler
from guiHandler import AuthField, EditPopUp, YesNoPopUpWindow, AddField, RegisterTOTPWindow, RegisterWindow, LoginPopUp
import toml, customtkinter as ctk, threading, os, pyotp, itertools, re, platform, base64, time, platform
from PIL import ImageTk

root = ctk.CTk()
path = os.path.dirname(os.path.abspath(__file__))
configPath = f"{path}/../resources/config.toml"
if not os.path.isfile(configPath):
 raise CriticalConfigError("[CRITICAL] Some moron deleted config.toml/preset.toml. If you are the moron, get these files, or reinstall")
secrets = {}
fields = {}
editFieldTxtVar = ctk.StringVar()

def _on_mousewheel(event):
 if platform.system() in ["Windows", "Darwin"]:
  sFrame._parent_canvas.yview_scroll(-1*(event.delta//120), "units")
 else:
  if event.num == 4:
   sFrame._parent_canvas.yview_scroll(-1, "units")
  elif event.num == 5:
   sFrame._parent_canvas.yview_scroll(1, "units")

def bind(parent, dict: dict):
 if 2 in dict:
  if platform.system() in ["Windows", "Darwin"]:
   parent._parent_canvas.bind_all("<MouseWheel>", _on_mousewheel)
  else:
   parent._parent_canvas.bind_all("<Button-4>", _on_mousewheel)
   parent._parent_canvas.bind_all("<Button-5>", _on_mousewheel)

def unbind(parent, dict:dict):
 if 2 not in dict:
  if platform.system() in ["Windows", "Darwin"]:
   parent._parent_canvas.unbind_all("<MouseWheel>")
  else:
   parent._parent_canvas.unbind_all("<Button-4>")
   parent._parent_canvas.unbind_all("<Button-5>")

def checkSecret(secret: str) -> bool:
 try:
  base64.b32decode(secret, casefold=True)
  _ = pyotp.TOTP(secret)
  return True
 except Exception:
  return False

def mainTOTPloop(secrets: dict, dict: dict):
 """EXECUTE ONLY AS A THREAD
 """
 while True:
  for i in sorted(dict):
   totp = pyotp.TOTP(secrets[i])
   e = dict[i].code
   e.configure(state="normal")
   e.delete(0, "end")
   e.insert(0, str(totp.now()))
   e.configure(state="readonly")
  time.sleep(0.5)


if __name__ == "__main__":
 root.geometry('430x600')
 root.resizable(False, False)
 root.title("btotp")
 if platform.system() == "Windows":
  root.iconbitmap(True, fr"{path}\..\resources\icon.ico")
 else:
  root.wm_iconphoto(True, ImageTk.PhotoImage(file=f"{path}/../resources/icon.png"))
 config = toml.load(configPath)
 wtxt = ctk.CTkLabel(root, text="", font=("Times New Roman", 40), anchor="w")
 wtxt.pack(pady=10)
 sFrame = ctk.CTkScrollableFrame(root, width=430, height=500)
 sFrame.pack(pady=20, fill="both", expand=True)
 addf = ""
 secretVar = ctk.StringVar()
 titleVar = ctk.StringVar()

 def editFieldFinalize(iN: int, newTitle: str, field_dict):
  field_dict[iN].codelabel.configure(text=newTitle)
  ConfigHandler().changeTitle(newTitle, iN)

 def editField(parent, key, titleVar, dict):
  ins = EditPopUp(parent, titleVar)
  def save_and_destroy():
   editFieldFinalize(key, titleVar.get(), dict)
   ins.destroy()
  ins.yes.configure(command=save_and_destroy)

 def addAField(dict: dict, 
               addFieldInstance: any, 
               secret: str, 
               title: str, 
               parent: any, 
               root: any, 
               password: str, 
               secretdict: dict, 
               regInstance: any
              ):
  if checkSecret(secret):
   lkey = next(i for i in itertools.count(0) if i not in dict)
   addFieldInstance.pack_forget()
   dict[lkey] = AuthField(parent, 
                          lambda lkey=lkey: editField(root, dict[lkey].key, editFieldTxtVar, dict),
                          lambda lkey=lkey: delField(lkey, dict, secretdict, root, parent), 
                          root, 
                          lkey
                         )
   dict[lkey].codelabel.configure(text=title)
   SecretHandler().secretRegister(password, secret, lkey)
   ConfigHandler().createField(lkey, title)
   secretdict[lkey] = secret
   dict[lkey].pack()
   addFieldInstance.pack()
   bind(parent,dict)
   regInstance.destroy()
  else:
   regInstance.output.configure(text="invalid TOTP secret!")

 def addFieldwin(parent, secretVar, titleVar, addCmd):
  regInstance = RegisterTOTPWindow(parent, secretVar, titleVar, None)
  regInstance.submit.configure(command=lambda: addCmd(regInstance))
  return regInstance

 def loadFields(dict: dict, parent, root, password: str, secretdict: dict):
  nums = [int(m.group(1)) for k in config if (m := re.match(r"^Field(\d+)$", k))]
  if nums:
   for i in range(min(nums), max(nums) + 1):
    title = ""
    secret = ""
    if f"Field{i}" in config:
     title = config[f"Field{i}"]['title']
     if f"field{i}" in config['secrets']:
      secret = SecretHandler().secretGet(password,i)
    dict[i] = AuthField(parent, 
                        lambda i=i: editField(root, dict[i].key, editFieldTxtVar, dict), 
                        lambda i=i: delField(i, dict, secretdict, root, parent), 
                        root, 
                        i
                       )
    dict[i].codelabel.configure(text=title)
    secretdict[i] = secret
    dict[i].pack()
  bind(parent,dict)

 def delField(iN, dict:dict, secrets:dict, root, parent):
  YesNoPopUpWindow(root,"Are you sure?","Are you sure?", lambda: delFieldFinalize(iN, dict, secrets, parent))

 def delFieldFinalize(iN, dict:dict, secrets:dict, parent):
  dict[iN].pack_forget()
  del dict[iN]
  del secrets[iN]
  ConfigHandler().deleteField(iN)
  SecretHandler().secretDelete(iN)
  unbind(parent, dict)

 if "firstRun" in config:
  newPwd = ctk.StringVar()
  newUsr = ctk.StringVar()
  def register(usr, pwd, regInstance):
   if usr.get() and pwd.get() and not any(ch.isspace() for ch in usr.get()) and not any(ch.isspace() for ch in pwd.get()):
    ConfigHandler().createBasicInfo(usr.get())
    SecretHandler().addHeading()
    SecretHandler().testEncode(pwd.get())
    regInstance.destroy()
    wtxt.configure(text=f"Welcome, {usr.get()}")
    addf = AddField(sFrame, lambda: addFieldwin(root, secretVar, titleVar, lambda regInstance: addAField(fields, addf, secretVar.get(), titleVar.get(), sFrame, root, newPwd.get(), secrets, regInstance)))
    addf.pack()
    threading.Thread(target=lambda: mainTOTPloop(secrets, fields), daemon=True).start()
  reg = RegisterWindow(root, newPwd, newUsr, lambda: register(newUsr, newPwd, reg))
 else:
  iPwd = ctk.StringVar()
  iUsr = ctk.StringVar()
  def login(pwd, usr, loginInstance):
   if config['BasicInformation']['accountName'] == usr.get():
    decodedTest = ""
    try:
     decodedTest = SecretHandler().testGet(pwd.get())
    except:
     print("username and/or password wrong")
     loginInstance.output.configure(text="username and/or password wrong")
    if decodedTest == "123qwerty":
     loginInstance.destroy()
     wtxt.configure(text=f"Welcome, {config['BasicInformation']['accountName']}")
     loadFields(fields, sFrame, root, iPwd.get(), secrets)
     addf = AddField(sFrame, lambda: addFieldwin(root, secretVar, titleVar, lambda regInstance: addAField(fields, addf, secretVar.get(), titleVar.get(), sFrame, root, iPwd.get(), secrets, regInstance)))
     addf.pack()
     threading.Thread(target=lambda: mainTOTPloop(secrets, fields), daemon=True).start()
   else:
    loginInstance.output.configure(text="username and/or password wrong")
  logini = LoginPopUp(root, iUsr, iPwd, lambda: login(iPwd, iUsr, logini), lambda: ConfigHandler().deleteConfig())
 root.mainloop()
