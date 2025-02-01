# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'filter_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_FilterDialog(object):
    def setupUi(self, FilterDialog):
        if not FilterDialog.objectName():
            FilterDialog.setObjectName(u"FilterDialog")
        FilterDialog.resize(480, 152)
        self.verticalLayout = QVBoxLayout(FilterDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(FilterDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fieldCombo = QComboBox(FilterDialog)
        self.fieldCombo.addItem("")
        self.fieldCombo.addItem("")
        self.fieldCombo.addItem("")
        self.fieldCombo.addItem("")
        self.fieldCombo.setObjectName(u"fieldCombo")

        self.horizontalLayout.addWidget(self.fieldCombo)

        self.verbCombo = QComboBox(FilterDialog)
        self.verbCombo.addItem("")
        self.verbCombo.addItem("")
        self.verbCombo.addItem("")
        self.verbCombo.addItem("")
        self.verbCombo.setObjectName(u"verbCombo")

        self.horizontalLayout.addWidget(self.verbCombo)

        self.queryStrEdit = QLineEdit(FilterDialog)
        self.queryStrEdit.setObjectName(u"queryStrEdit")

        self.horizontalLayout.addWidget(self.queryStrEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_2 = QLabel(FilterDialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.actionCombo = QComboBox(FilterDialog)
        self.actionCombo.addItem("")
        self.actionCombo.addItem("")
        self.actionCombo.addItem("")
        self.actionCombo.setObjectName(u"actionCombo")

        self.verticalLayout.addWidget(self.actionCombo)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(FilterDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.queryStrEdit, self.fieldCombo)
        QWidget.setTabOrder(self.fieldCombo, self.verbCombo)
        QWidget.setTabOrder(self.verbCombo, self.actionCombo)
        QWidget.setTabOrder(self.actionCombo, self.buttonBox)

        self.retranslateUi(FilterDialog)
        self.buttonBox.accepted.connect(FilterDialog.accept)
        self.buttonBox.rejected.connect(FilterDialog.reject)

        QMetaObject.connectSlotsByName(FilterDialog)
    # setupUi

    def retranslateUi(self, FilterDialog):
        FilterDialog.setWindowTitle(QCoreApplication.translate("FilterDialog", u"Create Filter", None))
        self.label.setText(QCoreApplication.translate("FilterDialog", u"When...", None))
        self.fieldCombo.setItemText(0, QCoreApplication.translate("FilterDialog", u"Title", None))
        self.fieldCombo.setItemText(1, QCoreApplication.translate("FilterDialog", u"Author", None))
        self.fieldCombo.setItemText(2, QCoreApplication.translate("FilterDialog", u"Description", None))
        self.fieldCombo.setItemText(3, QCoreApplication.translate("FilterDialog", u"Categories", None))

        self.verbCombo.setItemText(0, QCoreApplication.translate("FilterDialog", u"contains", None))
        self.verbCombo.setItemText(1, QCoreApplication.translate("FilterDialog", u"does not contain", None))
        self.verbCombo.setItemText(2, QCoreApplication.translate("FilterDialog", u"exactly equals", None))
        self.verbCombo.setItemText(3, QCoreApplication.translate("FilterDialog", u"matches by regular expression", None))

        self.label_2.setText(QCoreApplication.translate("FilterDialog", u"then...", None))
        self.actionCombo.setItemText(0, QCoreApplication.translate("FilterDialog", u"Copy to Items of Interest Feed", None))
        self.actionCombo.setItemText(1, QCoreApplication.translate("FilterDialog", u"Mark As Read", None))
        self.actionCombo.setItemText(2, QCoreApplication.translate("FilterDialog", u"Delete Item", None))

    # retranslateUi

