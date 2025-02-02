# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PrefsDlg.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_PrefsDlg(object):
    def setupUi(self, PrefsDlg):
        if not PrefsDlg.objectName():
            PrefsDlg.setObjectName(u"PrefsDlg")
        PrefsDlg.resize(395, 492)
        icon = QIcon()
        icon.addFile(u"Resources/RssReader.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        PrefsDlg.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(PrefsDlg)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_12 = QLabel(PrefsDlg)
        self.label_12.setObjectName(u"label_12")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        self.label_12.setFont(font)

        self.verticalLayout.addWidget(self.label_12)

        self.line_5 = QFrame(PrefsDlg)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_5)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.updateOnStartCheckbox = QCheckBox(PrefsDlg)
        self.updateOnStartCheckbox.setObjectName(u"updateOnStartCheckbox")

        self.horizontalLayout_5.addWidget(self.updateOnStartCheckbox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(PrefsDlg)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.intervalSpin = QSpinBox(PrefsDlg)
        self.intervalSpin.setObjectName(u"intervalSpin")
        self.intervalSpin.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.intervalSpin.setMinimum(1)
        self.intervalSpin.setMaximum(9999)
        self.intervalSpin.setValue(30)

        self.horizontalLayout.addWidget(self.intervalSpin)

        self.label_2 = QLabel(PrefsDlg)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_5)

        self.label_11 = QLabel(PrefsDlg)
        self.label_11.setObjectName(u"label_11")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.label_11.setFont(font1)

        self.verticalLayout.addWidget(self.label_11)

        self.line_4 = QFrame(PrefsDlg)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.minimizeOnFocusOutCheckbox = QCheckBox(PrefsDlg)
        self.minimizeOnFocusOutCheckbox.setObjectName(u"minimizeOnFocusOutCheckbox")

        self.horizontalLayout_3.addWidget(self.minimizeOnFocusOutCheckbox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label_5 = QLabel(PrefsDlg)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.verticalLayout.addWidget(self.label_5)

        self.line = QFrame(PrefsDlg)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(PrefsDlg)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.directoryLineEdit = QLineEdit(PrefsDlg)
        self.directoryLineEdit.setObjectName(u"directoryLineEdit")

        self.horizontalLayout_2.addWidget(self.directoryLineEdit)

        self.browseButton = QPushButton(PrefsDlg)
        self.browseButton.setObjectName(u"browseButton")

        self.horizontalLayout_2.addWidget(self.browseButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.useEnclosureSubdirectories = QCheckBox(PrefsDlg)
        self.useEnclosureSubdirectories.setObjectName(u"useEnclosureSubdirectories")
        self.useEnclosureSubdirectories.setEnabled(False)

        self.verticalLayout.addWidget(self.useEnclosureSubdirectories)

        self.verticalSpacer_4 = QSpacerItem(20, 14, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.label_6 = QLabel(PrefsDlg)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.verticalLayout.addWidget(self.label_6)

        self.line_2 = QFrame(PrefsDlg)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.formLayout = QFormLayout()
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(3)
        self.label_7 = QLabel(PrefsDlg)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_7)

        self.proxyTypeCombo = QComboBox(PrefsDlg)
        self.proxyTypeCombo.addItem("")
        self.proxyTypeCombo.addItem("")
        self.proxyTypeCombo.addItem("")
        self.proxyTypeCombo.addItem("")
        self.proxyTypeCombo.setObjectName(u"proxyTypeCombo")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.proxyTypeCombo)

        self.label_10 = QLabel(PrefsDlg)
        self.label_10.setObjectName(u"label_10")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_10)

        self.proxyHostnameLineEdit = QLineEdit(PrefsDlg)
        self.proxyHostnameLineEdit.setObjectName(u"proxyHostnameLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.proxyHostnameLineEdit)

        self.label_8 = QLabel(PrefsDlg)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_8)

        self.proxyPortSpinBox = QSpinBox(PrefsDlg)
        self.proxyPortSpinBox.setObjectName(u"proxyPortSpinBox")
        self.proxyPortSpinBox.setMaximum(99999)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.proxyPortSpinBox)

        self.label_9 = QLabel(PrefsDlg)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_9)

        self.proxyUserIdLineEdit = QLineEdit(PrefsDlg)
        self.proxyUserIdLineEdit.setObjectName(u"proxyUserIdLineEdit")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.proxyUserIdLineEdit)

        self.label_13 = QLabel(PrefsDlg)
        self.label_13.setObjectName(u"label_13")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_13)

        self.proxyPasswordLineEdit = QLineEdit(PrefsDlg)
        self.proxyPasswordLineEdit.setObjectName(u"proxyPasswordLineEdit")
        self.proxyPasswordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.proxyPasswordLineEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.label_4 = QLabel(PrefsDlg)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.verticalLayout.addWidget(self.label_4)

        self.line_3 = QFrame(PrefsDlg)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.loggingLevelComboBox = QComboBox(PrefsDlg)
        self.loggingLevelComboBox.addItem("")
        self.loggingLevelComboBox.addItem("")
        self.loggingLevelComboBox.addItem("")
        self.loggingLevelComboBox.addItem("")
        self.loggingLevelComboBox.addItem("")
        self.loggingLevelComboBox.addItem("")
        self.loggingLevelComboBox.addItem("")
        self.loggingLevelComboBox.setObjectName(u"loggingLevelComboBox")

        self.horizontalLayout_4.addWidget(self.loggingLevelComboBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(PrefsDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(PrefsDlg)
        self.buttonBox.rejected.connect(PrefsDlg.reject)
        self.buttonBox.accepted.connect(PrefsDlg.accept)

        self.loggingLevelComboBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PrefsDlg)
    # setupUi

    def retranslateUi(self, PrefsDlg):
        PrefsDlg.setWindowTitle(QCoreApplication.translate("PrefsDlg", u"Preferences", None))
        self.label_12.setText(QCoreApplication.translate("PrefsDlg", u"Feeds", None))
        self.updateOnStartCheckbox.setText(QCoreApplication.translate("PrefsDlg", u"Update feeds on startup", None))
        self.label.setText(QCoreApplication.translate("PrefsDlg", u"Update Feeds Every", None))
        self.label_2.setText(QCoreApplication.translate("PrefsDlg", u"minutes", None))
        self.label_11.setText(QCoreApplication.translate("PrefsDlg", u"User Interface", None))
        self.minimizeOnFocusOutCheckbox.setText(QCoreApplication.translate("PrefsDlg", u"Minimize App when Lose Focus", None))
        self.label_5.setText(QCoreApplication.translate("PrefsDlg", u"Enclosures", None))
        self.label_3.setText(QCoreApplication.translate("PrefsDlg", u"Enclosure Directory", None))
        self.browseButton.setText(QCoreApplication.translate("PrefsDlg", u"Browse...", None))
        self.useEnclosureSubdirectories.setText(QCoreApplication.translate("PrefsDlg", u"Use separate subdirectory for each feed", None))
        self.label_6.setText(QCoreApplication.translate("PrefsDlg", u"HTTP Proxy", None))
        self.label_7.setText(QCoreApplication.translate("PrefsDlg", u"Proxy type", None))
        self.proxyTypeCombo.setItemText(0, QCoreApplication.translate("PrefsDlg", u"None", None))
        self.proxyTypeCombo.setItemText(1, QCoreApplication.translate("PrefsDlg", u"Socks5", None))
        self.proxyTypeCombo.setItemText(2, QCoreApplication.translate("PrefsDlg", u"HTML", None))
        self.proxyTypeCombo.setItemText(3, QCoreApplication.translate("PrefsDlg", u"HTML Cached", None))

        self.label_10.setText(QCoreApplication.translate("PrefsDlg", u"Proxy host name", None))
        self.label_8.setText(QCoreApplication.translate("PrefsDlg", u"Proxy port", None))
        self.label_9.setText(QCoreApplication.translate("PrefsDlg", u"Proxy user ID", None))
        self.label_13.setText(QCoreApplication.translate("PrefsDlg", u"Proxy password", None))
        self.label_4.setText(QCoreApplication.translate("PrefsDlg", u"Logging level", None))
        self.loggingLevelComboBox.setItemText(0, QCoreApplication.translate("PrefsDlg", u"Trace", None))
        self.loggingLevelComboBox.setItemText(1, QCoreApplication.translate("PrefsDlg", u"Debug", None))
        self.loggingLevelComboBox.setItemText(2, QCoreApplication.translate("PrefsDlg", u"Info", None))
        self.loggingLevelComboBox.setItemText(3, QCoreApplication.translate("PrefsDlg", u"Warn", None))
        self.loggingLevelComboBox.setItemText(4, QCoreApplication.translate("PrefsDlg", u"Error", None))
        self.loggingLevelComboBox.setItemText(5, QCoreApplication.translate("PrefsDlg", u"Fatal", None))
        self.loggingLevelComboBox.setItemText(6, QCoreApplication.translate("PrefsDlg", u"None", None))

    # retranslateUi

