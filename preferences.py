# Preferences
from encrypter import Encrypter
import logging

class Preferences:
    def __init__(self):
        self.encrypter = Encrypter()

        # Initialize default preferences
        self.feedUpdateInterval = 30
        self.updateOnAppStart = False
        self.minimizeAppOnLoseFocus = False
        self.enclosureDirectory = ""
        self.encryptedInstapaperUsername = b''       # This is stored encrypted
        self.encryptedInstapaperPassword = b''       # This is stored encrypted

        # The encrypter password is used to encrypt/decrypt Instapaper credentials.
        # It is stored hashed to be able to verify that the password entered by the user is correct.
        self.hashedEncrypterPassword = ""           # This is stored hashed

    def getInstapaperUsername(self):
        """ Returns the decrypted Instapaper username. """
        if not self.encrypter.hasPassword:
            logging.error("[Preferences.getInstapaperUsername] Encrypter password has not been set")
            raise ValueError("Encrypter password has not been set")

        return self.encrypter.decrypt(self.encryptedInstapaperUsername)

    def setEncryptedInstapaperUsername(self, username: str):
        """ Sets the Instapaper username, encrypting it before storage. """
        if not self.encrypter.hasPassword:
            logging.error("[Preferences.setEncryptedInstapaperUsername] Encrypter password has not been set")
            raise ValueError("Encrypter password has not been set")

        self.encryptedInstapaperUsername = self.encrypter.encrypt(username)

    def getInstapaperPassword(self):
        """ Returns the decrypted Instapaper password. """
        if not self.encrypter.hasPassword:
            logging.error("[Preferences.getInstapaperPassword] Encrypter password has not been set")
            raise ValueError("Encrypter password has not been set")

        return self.encrypter.decrypt(self.encryptedInstapaperPassword)

    def setEncryptedInstapaperPassword(self, password: str):
        """ Sets the Instapaper password, encrypting it before storage. """
        if not self.encrypter.hasPassword:
            logging.error("[Preferences.setEncryptedInstapaperPassword] Encrypter password has not been set")
            raise ValueError("Encrypter password has not been set")

        self.encryptedInstapaperPassword = self.encrypter.encrypt(password)

    def setEncrypterPassword(self, plainTextPassword: str):
        """ Sets the encrypter password.  This is stored hashed, and is used to verify
            that the user-entered password is correct. """
        if len(plainTextPassword) == 0:
            logging.error("[Preferences.setEncrypterPassword] Encrypter password cannot be empty")
            raise ValueError("Encrypter password cannot be empty")

        self.encrypter.setPassword(plainTextPassword)
        self.hashedEncrypterPassword = self.encrypter.hashedPassword()

    @property
    def hasValidEncrypterPassword(self):
        return len(self.hashedEncrypterPassword) > 0

    @property
    def hasEncrypterPassword(self) -> bool:
        return self.encrypter.hasPassword

    @property
    def hasInstapaperCredentials(self) -> bool:
        return len(self.encryptedInstapaperUsername) > 0 and len(self.encryptedInstapaperPassword) > 0

    def verifyEncrypterPassword(self, plainTextPassword: str) -> bool:
        """ Verifies that the provided password matches the stored hashed password. """
        if len(self.hashedEncrypterPassword) == 0:
            logging.error("[Preferences.verifyEncrypterPassword] No encrypter password has been set")
            raise ValueError("No encrypter password has been set")

        tempEncrypter = Encrypter()
        tempEncrypter.setPassword(plainTextPassword)
        tempEncrypterPasswordHash = tempEncrypter.hashedPassword()
        return tempEncrypterPasswordHash == self.hashedEncrypterPassword
