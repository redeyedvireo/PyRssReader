# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PurgeDlg.ui'
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
    QHBoxLayout, QLabel, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_PurgeDlg(object):
    def setupUi(self, PurgeDlg):
        if not PurgeDlg.objectName():
            PurgeDlg.setObjectName(u"PurgeDlg")
        PurgeDlg.resize(237, 138)
        icon = QIcon()
        icon.addFile(u"Resources/RssReader.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        PurgeDlg.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(PurgeDlg)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(PurgeDlg)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.daysSpin = QSpinBox(PurgeDlg)
        self.daysSpin.setObjectName(u"daysSpin")
        self.daysSpin.setMinimum(1)
        self.daysSpin.setMaximum(9999)
        self.daysSpin.setValue(10)

        self.horizontalLayout.addWidget(self.daysSpin)

        self.label_2 = QLabel(PurgeDlg)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.deleteReadOnlyButton = QRadioButton(PurgeDlg)
        self.deleteReadOnlyButton.setObjectName(u"deleteReadOnlyButton")
        self.deleteReadOnlyButton.setChecked(True)

        self.verticalLayout.addWidget(self.deleteReadOnlyButton)

        self.deleteReadAndUnreadButton = QRadioButton(PurgeDlg)
        self.deleteReadAndUnreadButton.setObjectName(u"deleteReadAndUnreadButton")

        self.verticalLayout.addWidget(self.deleteReadAndUnreadButton)

        self.verticalSpacer = QSpacerItem(20, 14, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(PurgeDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(PurgeDlg)
        self.buttonBox.accepted.connect(PurgeDlg.accept)
        self.buttonBox.rejected.connect(PurgeDlg.reject)

        QMetaObject.connectSlotsByName(PurgeDlg)
    # setupUi

    def retranslateUi(self, PurgeDlg):
        PurgeDlg.setWindowTitle(QCoreApplication.translate("PurgeDlg", u"Purge Feed", None))
        self.label.setText(QCoreApplication.translate("PurgeDlg", u"Delete older than", None))
        self.label_2.setText(QCoreApplication.translate("PurgeDlg", u"days", None))
        self.deleteReadOnlyButton.setText(QCoreApplication.translate("PurgeDlg", u"Delete read messages only", None))
        self.deleteReadAndUnreadButton.setText(QCoreApplication.translate("PurgeDlg", u"Delete read and unread messages", None))
    # retranslateUi

