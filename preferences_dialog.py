from PyQt5 import uic, QtWidgets
from proxy import Proxy


class PrefsDialog(QtWidgets.QDialog):
    def __init__(self, parent, proxy):
        super(PrefsDialog, self).__init__(parent)
        uic.loadUi('PrefsDlg.ui', self)
        self.proxy = proxy

        self.populate()

    def populate(self):
        self.proxyHostnameLineEdit.setText(self.proxy.proxyUrl)
        self.proxyPortSpinBox.setValue(self.proxy.proxyPort)
        self.proxyUserIdLineEdit.setText(self.proxy.proxyUser)

        # Set proxy type to HTML, and disable it.
        self.proxyTypeCombo.setCurrentIndex(2)
        self.proxyTypeCombo.setEnabled(False)

    def getProxySettings(self):
        """ Returns a Proxy object containing settings from the dialog. """
        self.proxy.proxyUrl = self.proxyHostnameLineEdit.text()
        self.proxy.proxyPort = self.proxyPortSpinBox.value()
        self.proxy.proxyUser = self.proxyUserIdLineEdit.text()
        return self.proxy
