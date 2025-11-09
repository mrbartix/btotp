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
import toml, os, hashlib, base64
from cryptography.fernet import Fernet, InvalidToken

class ConfigError(Exception):
 pass
class CriticalConfigError(Exception):
 pass

class ConfigHandler:
 """Handles the config
 """
 def __init__(self):
  self.path = os.path.dirname(os.path.abspath(__file__))
  self.configPath = f"{self.path}/../resources/config.toml"
  self.presetPath = f"{self.path}/../resources/presets.toml"
  if not os.path.isfile(self.configPath) or not os.path.isfile(self.presetPath):
   raise CriticalConfigError("[CRITICAL] Some moron deleted config.toml/preset.toml. If you are the moron, get these files, or reinstall")
 def fieldWriteTitle(self, fieldNumber: int, newTitle: str) -> None:
  config = toml.load(self.configPath)
  if f'Field{fieldNumber}' in config.keys():
   config[f'Field{fieldNumber}']['title'] = newTitle
   with open(self.configPath, "w") as f:
    toml.dump(config, f)
    f.close()
  else:
   raise ConfigError(f"Field{fieldNumber} does not exist. Create it first!")
 def createField(self, fieldNumber : int, title: str) -> None:
  """Creates a field with information about it
  Args:
   fieldNumber (int): What number is the field saved as
   *title (str): optional, but VERY recomended
  """
  config = toml.load(self.configPath)
  preset = toml.load(self.presetPath)
  if not config['BasicInformation']:
   raise ConfigError("No BasicInformation, make sure to create it before running fieldCreate()")
  newFieldNo = f'Field{fieldNumber}'
  new = preset.pop("FieldNo")
  new['title'] = title
  config[newFieldNo] = new
  with open(self.configPath, "w") as f:
   toml.dump(config, f)
   f.close()
 def createBasicInfo(self, name: str) -> None:
  """Creates BasicInformation field
  Args:
   name (str): username
  """
  config = toml.load(self.configPath) # i dont really care that im repeating myself
  preset = toml.load(self.presetPath)
  if "BasicInformation" not in config:
   if config['firstRun']:
    del config['firstRun']
   preset['BasicInformation']['accountName'] = name
   config['BasicInformation'] = preset['BasicInformation']
   with open(self.configPath, "w") as f:
    toml.dump(config, f)
    f.close()
  else:
   raise ConfigError("BasicInformation already exists you donut")
 def changeTitle(self, newTitle: str, fieldNumber: int) -> None:
  """Edit some fields title
  Args:
   newTitle (str): The new title
   fieldNumber (int): The number of the field you want to edit
  """
  config = toml.load(self.configPath)
  if f"Field{fieldNumber}" in config:
   config[f'Field{fieldNumber}']['title'] = newTitle
   with open(self.configPath, "w") as f:
    toml.dump(config, f)
    f.close()
  else: raise ConfigError(f"Field{fieldNumber} does not exit, create it first")
 def deleteConfig(self) -> None:
  """Deletes the whole config
  """
  with open(self.configPath, "w") as f:
   toml.dump({"firstRun": True}, f)
   f.close()
 def deleteField(self, fieldNumber: int) -> None:
  """Deletes a field
  Args:
   fieldNumber (int): number of the field you want to delete
  """
  config = toml.load(self.configPath)
  if config[f'Field{fieldNumber}']:
   del config[f'Field{fieldNumber}']
  else: raise ConfigError(f"Field{fieldNumber} does not exist")
  with open(self.configPath, "w") as f:
   toml.dump(config, f)
   f.close()

class SecretHandler:
 """Handles the secret encryption/decryption
 """
 def __init__(self):
  self.path = os.path.dirname(os.path.abspath(__file__))
  self.configPath = f"{self.path}/../resources/config.toml"
  self.presetPath = f"{self.path}/../resources/presets.toml"
  if not os.path.isfile(self.configPath) or not os.path.isfile(self.presetPath):
   raise CriticalConfigError("[CRITICAL] Some moron deleted config.toml/preset.toml. If you are the moron, get these files, or reinstall")
 def addHeading(self) -> None:
  """Adds a heading called 'secrets'
  This heading needs to be created if you want to add a secret
  """
  preset = toml.load(self.presetPath)
  config = toml.load(self.configPath)
  if "firstRun" not in config:
   config['secrets'] = preset['secrets']
   with open(self.configPath, "w") as f:
    toml.dump(config, f)
    f.close()
  else: raise ConfigError("firstRun exists, that means that user is not registered")
 def testEncode(self, password: str):
  """Encrypts a test string and puts it into the config
  Args:
   password (str): The password which is going to be used as the key
  """
  config = toml.load(self.configPath)
  if 'secrets' in config:
   fKey = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
   fernet = Fernet(fKey)
   tstr = "123qwerty"
   config['secrets']['test'] = fernet.encrypt(tstr.encode()).decode()
   with open(self.configPath, "w") as f:
    toml.dump(config, f)
    f.close()
  else: raise ConfigError("section 'secrets' in the config does not exist")
 def testGet(self, password: str) -> str:
  """Reads and decrypts the test encoded string from the config
  Args:
   password (str): The password which is going to be used as the key
  """
  config = toml.load(self.configPath)
  if 'secrets' in config:
   if config['secrets']['test']:
    fKey = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
    fernet = Fernet(fKey)
    encryptedSecret = config['secrets']['test']
    try:
     dSecret = fernet.decrypt(encryptedSecret)
     return dSecret.decode()
    except InvalidToken:
     raise ConfigError("invalid password! unable to decrypt the test")
   else: raise ConfigError("the test string does not exist!")
  else: raise ConfigError("section 'secret' in the config does not exist!")
 def secretRegister(self, password: str, secret: str, instanceNumber: int) -> None:
  """Adds, encrypts and writes a secret TOTP string to the config
  Args:
   password (str): The password which is going to be used as the key
   secret (str): The TOTP secret which is going to be encrypted and written to the config
   instanceNumber (int): Number of the field (used for creating the field)
  """
  config = toml.load(self.configPath)
  if 'secrets' in config:
   fKey = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
   fernet = Fernet(fKey)
   config['secrets'][f'field{instanceNumber}'] = fernet.encrypt(secret.encode()).decode()
   with open(self.configPath, "w") as f:
    toml.dump(config, f)
    f.close()
  else: raise ConfigError("section 'secrets' in the config does not exist")
 def secretGet(self, password: str, instanceNumber: int) -> str:
  """Reads and decrypts a secret TOTP string from the config
  Args:
   password (str): The password which is going to be used as the key
   instanceNumber (int): Number of the field (used for creating the field)
  """
  config = toml.load(self.configPath)
  if 'secrets' in config:
   if config['secrets'][f'field{instanceNumber}']:
    fKey = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
    fernet = Fernet(fKey)
    encryptedSecret = config['secrets'][f'field{instanceNumber}']
    try:
     dSecret = fernet.decrypt(encryptedSecret)
     return dSecret.decode()
    except InvalidToken:
     raise ConfigError("invalid password! unable to decrypt secret")
   else: raise ConfigError(f"field{instanceNumber} does not exist!")
  else: raise ConfigError("section 'secret' in the config does not exist!")
 def secretDelete(self, instanceNumber: int):
  """Deletes a secret from the config
  """
  config = toml.load(self.configPath)
  if config['secrets'][f'field{instanceNumber}']:
   del config['secrets'][f'field{instanceNumber}']
   with open(self.configPath, "w") as f:
    toml.dump(config, f)
    f.close()
  else: raise ConfigError(f"field{instanceNumber} does not exist!")
