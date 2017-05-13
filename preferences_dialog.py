from PyQt5 import uic, QtCore, QtWidgets
from proxy import Proxy


class PrefsDialog(QtWidgets.QDialog):
    def __init__(self, parent, proxy, preferences):
        super(PrefsDialog, self).__init__(parent)
        uic.loadUi('PrefsDlg.ui', self)
        self.proxy = proxy
        self.preferences = preferences

        self.populate()

    def populate(self):
        self.proxyHostnameLineEdit.setText(self.proxy.proxyUrl)
        self.proxyPortSpinBox.setValue(self.proxy.proxyPort)
        self.proxyUserIdLineEdit.setText(self.proxy.proxyUser)

        # Set proxy type to HTML, and disable it.
        self.proxyTypeCombo.setCurrentIndex(2)
        self.proxyTypeCombo.setEnabled(False)

        # Feed updating
        self.intervalSpin.setValue(self.preferences.feedUpdateInterval)
        self.updateOnStartCheckbox.setChecked(self.preferences.updateOnAppStart)

        self.minimizeOnFocusOutCheckbox.setChecked(self.preferences.minimizeAppOnLoseFocus)

        # Enclosures
        self.directoryLineEdit.setText(self.preferences.enclosureDirectory)

    @QtCore.pyqtSlot()
    def on_browseButton_clicked(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Enclosure Directory")
        if directory:
            self.directoryLineEdit.setText(directory)

    def getProxySettings(self):
        """ Returns a Proxy object containing settings from the dialog. """
        self.proxy.proxyUrl = self.proxyHostnameLineEdit.text()
        self.proxy.proxyPort = self.proxyPortSpinBox.value()
        self.proxy.proxyUser = self.proxyUserIdLineEdit.text()
        return self.proxy

    def getPreferences(self):
        """ Returns the feed update interval. """
        self.preferences.feedUpdateInterval = self.intervalSpin.value()
        self.preferences.updateOnAppStart = self.updateOnStartCheckbox.isChecked()
        self.preferences.minimizeAppOnLoseFocus = self.minimizeOnFocusOutCheckbox.isChecked()
        self.preferences.enclosureDirectory = self.directoryLineEdit.text()
        return self.preferences

