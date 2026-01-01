from PySide6 import QtWidgets
from ui_instapaper_credentials_dialog import Ui_InstapaperCredentialsDlg

class InstapaperCredentialsDialog(QtWidgets.QDialog):
  def __init__(self, parent):
    super(InstapaperCredentialsDialog, self).__init__(parent)

    self.ui = Ui_InstapaperCredentialsDlg()
    self.ui.setupUi(self)

  def getUsername(self):
    return self.ui.usernameEdit.text()

  def getPassword(self):
    return self.ui.passwordEdit.text()

  def getCredentials(self):
    return self.getUsername(), self.getPassword()
