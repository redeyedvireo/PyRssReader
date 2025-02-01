# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filter_manager_dialog.ui'
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
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_FilterManagerDlg(object):
    def setupUi(self, FilterManagerDlg):
        if not FilterManagerDlg.objectName():
            FilterManagerDlg.setObjectName(u"FilterManagerDlg")
        FilterManagerDlg.resize(680, 408)
        self.verticalLayout_2 = QVBoxLayout(FilterManagerDlg)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.label_2 = QLabel(FilterManagerDlg)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.filterList = QListWidget(FilterManagerDlg)
        self.filterList.setObjectName(u"filterList")

        self.horizontalLayout_2.addWidget(self.filterList)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.addButton = QPushButton(FilterManagerDlg)
        self.addButton.setObjectName(u"addButton")
        icon = QIcon()
        icon.addFile(u"Resources/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addButton.setIcon(icon)

        self.verticalLayout.addWidget(self.addButton)

        self.deleteButton = QPushButton(FilterManagerDlg)
        self.deleteButton.setObjectName(u"deleteButton")
        icon1 = QIcon()
        icon1.addFile(u"Resources/minus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deleteButton.setIcon(icon1)

        self.verticalLayout.addWidget(self.deleteButton)

        self.editButton = QPushButton(FilterManagerDlg)
        self.editButton.setObjectName(u"editButton")
        icon2 = QIcon()
        icon2.addFile(u"Resources/edit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.editButton.setIcon(icon2)

        self.verticalLayout.addWidget(self.editButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(FilterManagerDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(FilterManagerDlg)
        self.buttonBox.rejected.connect(FilterManagerDlg.reject)

        QMetaObject.connectSlotsByName(FilterManagerDlg)
    # setupUi

    def retranslateUi(self, FilterManagerDlg):
        FilterManagerDlg.setWindowTitle(QCoreApplication.translate("FilterManagerDlg", u"Global Filters", None))
        self.label_2.setText(QCoreApplication.translate("FilterManagerDlg", u"Current Filters:", None))
        self.addButton.setText("")
        self.deleteButton.setText("")
        self.editButton.setText("")
    # retranslateUi

