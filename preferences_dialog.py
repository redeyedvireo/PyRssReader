from PySide6 import QtCore, QtWidgets
from proxy import Proxy
from ui_PrefsDlg import Ui_PrefsDlg

class PrefsDialog(QtWidgets.QDialog):
    def __init__(self, parent, proxy: Proxy, preferences):
        super(PrefsDialog, self).__init__(parent)

        self.ui = Ui_PrefsDlg()
        self.ui.setupUi(self)

        self.proxy = proxy
        self.preferences = preferences

        self.populate()

    def populate(self):
        self.ui.proxyHostnameLineEdit.setText(self.proxy.proxyUrl)
        self.ui.proxyPortSpinBox.setValue(self.proxy.proxyPort)
        self.ui.proxyUserIdLineEdit.setText(self.proxy.proxyUser)
        self.ui.proxyPasswordLineEdit.setText(self.proxy.proxyPassword)

        # Set proxy type to HTML, and disable it.
        self.ui.proxyTypeCombo.setCurrentIndex(2)
        self.ui.proxyTypeCombo.setEnabled(False)

        # Feed updating
        self.ui.intervalSpin.setValue(self.preferences.feedUpdateInterval)
        self.ui.updateOnStartCheckbox.setChecked(self.preferences.updateOnAppStart)

        self.ui.minimizeOnFocusOutCheckbox.setChecked(self.preferences.minimizeAppOnLoseFocus)

        # Enclosures
        self.ui.directoryLineEdit.setText(self.preferences.enclosureDirectory)

    @QtCore.Slot()
    def on_browseButton_clicked(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Enclosure Directory")
        if directory:
            self.ui.directoryLineEdit.setText(directory)

    def getProxySettings(self):
        """ Returns a Proxy object containing settings from the dialog. """
        self.proxy.proxyUrl = self.ui.proxyHostnameLineEdit.text()
        self.proxy.proxyPort = self.ui.proxyPortSpinBox.value()
        self.proxy.proxyUser = self.ui.proxyUserIdLineEdit.text()
        self.proxy.proxyPassword = self.ui.proxyPasswordLineEdit.text()
        return self.proxy

    def getPreferences(self):
        """ Returns the feed update interval. """
        self.preferences.feedUpdateInterval = self.ui.intervalSpin.value()
        self.preferences.updateOnAppStart = self.ui.updateOnStartCheckbox.isChecked()
        self.preferences.minimizeAppOnLoseFocus = self.ui.minimizeOnFocusOutCheckbox.isChecked()
        self.preferences.enclosureDirectory = self.ui.directoryLineEdit.text()
        return self.preferences

