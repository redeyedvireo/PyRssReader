# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'language_filter_dialog.ui'
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
    QFrame, QHBoxLayout, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_LanguageFilterDlg(object):
    def setupUi(self, LanguageFilterDlg):
        if not LanguageFilterDlg.objectName():
            LanguageFilterDlg.setObjectName(u"LanguageFilterDlg")
        LanguageFilterDlg.resize(433, 395)
        self.verticalLayout = QVBoxLayout(LanguageFilterDlg)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listWidget = QListWidget(LanguageFilterDlg)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.deleteButton = QPushButton(LanguageFilterDlg)
        self.deleteButton.setObjectName(u"deleteButton")

        self.horizontalLayout_2.addWidget(self.deleteButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addWordEdit = QLineEdit(LanguageFilterDlg)
        self.addWordEdit.setObjectName(u"addWordEdit")

        self.horizontalLayout.addWidget(self.addWordEdit)

        self.addButton = QPushButton(LanguageFilterDlg)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout.addWidget(self.addButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.line = QFrame(LanguageFilterDlg)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.buttonBox = QDialogButtonBox(LanguageFilterDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(LanguageFilterDlg)
        self.buttonBox.rejected.connect(LanguageFilterDlg.reject)

        QMetaObject.connectSlotsByName(LanguageFilterDlg)
    # setupUi

    def retranslateUi(self, LanguageFilterDlg):
        LanguageFilterDlg.setWindowTitle(QCoreApplication.translate("LanguageFilterDlg", u"Edit Language Filter", None))
        self.deleteButton.setText(QCoreApplication.translate("LanguageFilterDlg", u"Delete", None))
        self.addButton.setText(QCoreApplication.translate("LanguageFilterDlg", u"Add", None))
    # retranslateUi

