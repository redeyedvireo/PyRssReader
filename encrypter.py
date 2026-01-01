import hashlib
import base64
import os
import logging
from typing import Final
import cryptography
from cryptography.fernet import Fernet
import cryptography.fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encrypter():
  SALT: Final[bytes] = bytes([10, 8, 99, 54, 23, 87, 45, 12, 67, 34, 90, 123, 210, 56, 78, 89])  # Random string of bytes

  def __init__(self) -> None:
    self.clear()

  @property
  def hasPassword(self) -> bool:
    return len(self.plainTextPassword) > 0

  def setPassword(self, plainTextPassword: str) -> None:
    self.plainTextPassword = plainTextPassword
    self.fernet = self.createFernet()

  def clear(self):
    self.plainTextPassword = ''
    self.fernet = None

  def hashedPassword(self):
    if len(self.plainTextPassword) == 0:
      raise ValueError("No password set")

    return self.hashValue(self.plainTextPassword)

  def hashValue(self, value: str) -> str:
    m = hashlib.sha256()
    valueAsBytes = value.encode('utf8')
    m.update(valueAsBytes)
    return m.hexdigest()

  def createFernet(self) -> Fernet | None:
    """ Creates a Fernet object, which is used to encrypt and decrypt messages.
        The password and salt must exist when calling this function.
    """
    if len(self.plainTextPassword) == 0:
      raise ValueError("Attempt to create Fernet with no password")

    passwordBytes = bytes(self.plainTextPassword, 'utf-8')

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=Encrypter.SALT,
        iterations=480000)

    key = base64.urlsafe_b64encode(kdf.derive(passwordBytes))
    return Fernet(key)

  def encrypt(self, contents: str) -> bytes:
    if len(self.plainTextPassword) == 0:
      raise ValueError("Attempt to encrypt with no password")

    if self.fernet is None:
      raise Exception('Encrypt: fernet not initialized.')

    contentsBytes = bytes(contents, 'utf-8')
    encryptedContents = self.fernet.encrypt(contentsBytes)

    return encryptedContents

  def decrypt(self, encryptedContents: bytes) -> str:
    if self.fernet is None:
      raise Exception('Decrypt: fernet not initialized.')

    try:
      decryptedContentsBytes = self.fernet.decrypt(encryptedContents)
      decryptedContentsStr = decryptedContentsBytes.decode()

    except TypeError as e:
      logging.error(f'[Encrypter.decrypt] Decryption error: {e}')
      return ''
    except cryptography.fernet.InvalidToken as e:
      logging.error(f'[Encrypter.decrypt] Invalid token: {e}')
      return ''

    return decryptedContentsStr
