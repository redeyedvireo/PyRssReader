# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'instapaper_credentials_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_InstapaperCredentialsDlg(object):
    def setupUi(self, InstapaperCredentialsDlg):
        if not InstapaperCredentialsDlg.objectName():
            InstapaperCredentialsDlg.setObjectName(u"InstapaperCredentialsDlg")
        InstapaperCredentialsDlg.resize(338, 158)
        self.verticalLayout = QVBoxLayout(InstapaperCredentialsDlg)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(InstapaperCredentialsDlg)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(InstapaperCredentialsDlg)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.usernameEdit = QLineEdit(InstapaperCredentialsDlg)
        self.usernameEdit.setObjectName(u"usernameEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.usernameEdit)

        self.label_3 = QLabel(InstapaperCredentialsDlg)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.passwordEdit = QLineEdit(InstapaperCredentialsDlg)
        self.passwordEdit.setObjectName(u"passwordEdit")
        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.passwordEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(InstapaperCredentialsDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(InstapaperCredentialsDlg)
        self.buttonBox.accepted.connect(InstapaperCredentialsDlg.accept)
        self.buttonBox.rejected.connect(InstapaperCredentialsDlg.reject)

        QMetaObject.connectSlotsByName(InstapaperCredentialsDlg)
    # setupUi

    def retranslateUi(self, InstapaperCredentialsDlg):
        InstapaperCredentialsDlg.setWindowTitle(QCoreApplication.translate("InstapaperCredentialsDlg", u"Instapaper Credentials", None))
        self.label.setText(QCoreApplication.translate("InstapaperCredentialsDlg", u"Instapaper Credentials", None))
        self.label_2.setText(QCoreApplication.translate("InstapaperCredentialsDlg", u"User name", None))
        self.label_3.setText(QCoreApplication.translate("InstapaperCredentialsDlg", u"Password", None))
    # retranslateUi

