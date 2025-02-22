# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ad_filter_dialog.ui'
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
    QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import PyRssReader_rc

class Ui_EditAdFilterDlg(object):
    def setupUi(self, EditAdFilterDlg):
        if not EditAdFilterDlg.objectName():
            EditAdFilterDlg.setObjectName(u"EditAdFilterDlg")
        EditAdFilterDlg.resize(435, 395)
        icon = QIcon()
        icon.addFile(u":/RssReader/Resources/RssReader.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        EditAdFilterDlg.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(EditAdFilterDlg)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listWidget = QListWidget(EditAdFilterDlg)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.deleteButton = QPushButton(EditAdFilterDlg)
        self.deleteButton.setObjectName(u"deleteButton")

        self.horizontalLayout.addWidget(self.deleteButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.addWordEdit = QLineEdit(EditAdFilterDlg)
        self.addWordEdit.setObjectName(u"addWordEdit")

        self.horizontalLayout_2.addWidget(self.addWordEdit)

        self.addButton = QPushButton(EditAdFilterDlg)
        self.addButton.setObjectName(u"addButton")

        self.horizontalLayout_2.addWidget(self.addButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.buttonBox = QDialogButtonBox(EditAdFilterDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(EditAdFilterDlg)
        self.buttonBox.rejected.connect(EditAdFilterDlg.reject)

        QMetaObject.connectSlotsByName(EditAdFilterDlg)
    # setupUi

    def retranslateUi(self, EditAdFilterDlg):
        EditAdFilterDlg.setWindowTitle(QCoreApplication.translate("EditAdFilterDlg", u"Edit Ad Filter", None))
        self.deleteButton.setText(QCoreApplication.translate("EditAdFilterDlg", u"Delete", None))
        self.addButton.setText(QCoreApplication.translate("EditAdFilterDlg", u"Add", None))
    # retranslateUi

