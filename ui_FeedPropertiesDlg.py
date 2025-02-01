# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FeedPropertiesDlg.ui'
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
    QFormLayout, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_CFeedPropertiesDlg(object):
    def setupUi(self, CFeedPropertiesDlg):
        if not CFeedPropertiesDlg.objectName():
            CFeedPropertiesDlg.setObjectName(u"CFeedPropertiesDlg")
        CFeedPropertiesDlg.resize(359, 183)
        icon = QIcon()
        icon.addFile(u"Resources/RssReader.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        CFeedPropertiesDlg.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(CFeedPropertiesDlg)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.feedIconLabel = QLabel(CFeedPropertiesDlg)
        self.feedIconLabel.setObjectName(u"feedIconLabel")

        self.horizontalLayout.addWidget(self.feedIconLabel)

        self.titleLabel = QLabel(CFeedPropertiesDlg)
        self.titleLabel.setObjectName(u"titleLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.titleLabel.setFont(font)

        self.horizontalLayout.addWidget(self.titleLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(3, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.urlLabel = QLabel(CFeedPropertiesDlg)
        self.urlLabel.setObjectName(u"urlLabel")

        self.horizontalLayout_2.addWidget(self.urlLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.formLayout = QFormLayout()
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(3)
        self.formLayout.setVerticalSpacing(3)
        self.label_3 = QLabel(CFeedPropertiesDlg)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.dateAddedLabel = QLabel(CFeedPropertiesDlg)
        self.dateAddedLabel.setObjectName(u"dateAddedLabel")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.dateAddedLabel)

        self.label_4 = QLabel(CFeedPropertiesDlg)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.lastUpdatedLabel = QLabel(CFeedPropertiesDlg)
        self.lastUpdatedLabel.setObjectName(u"lastUpdatedLabel")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lastUpdatedLabel)

        self.label_5 = QLabel(CFeedPropertiesDlg)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.lastPurgedLabel = QLabel(CFeedPropertiesDlg)
        self.lastPurgedLabel.setObjectName(u"lastPurgedLabel")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lastPurgedLabel)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 14, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.line = QFrame(CFeedPropertiesDlg)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.buttonBox = QDialogButtonBox(CFeedPropertiesDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(CFeedPropertiesDlg)
        self.buttonBox.accepted.connect(CFeedPropertiesDlg.accept)
        self.buttonBox.rejected.connect(CFeedPropertiesDlg.reject)

        QMetaObject.connectSlotsByName(CFeedPropertiesDlg)
    # setupUi

    def retranslateUi(self, CFeedPropertiesDlg):
        CFeedPropertiesDlg.setWindowTitle(QCoreApplication.translate("CFeedPropertiesDlg", u"Feed Properties", None))
        self.feedIconLabel.setText(QCoreApplication.translate("CFeedPropertiesDlg", u"-", None))
        self.titleLabel.setText(QCoreApplication.translate("CFeedPropertiesDlg", u"-", None))
        self.urlLabel.setText(QCoreApplication.translate("CFeedPropertiesDlg", u"-", None))
        self.label_3.setText(QCoreApplication.translate("CFeedPropertiesDlg", u"Date Added:", None))
        self.dateAddedLabel.setText(QCoreApplication.translate("CFeedPropertiesDlg", u"-", None))
        self.label_4.setText(QCoreApplication.translate("CFeedPropertiesDlg", u"Last Updated:", None))
        self.lastUpdatedLabel.setText(QCoreApplication.translate("CFeedPropertiesDlg", u"-", None))
        self.label_5.setText(QCoreApplication.translate("CFeedPropertiesDlg", u"Last Purged:", None))
        self.lastPurgedLabel.setText(QCoreApplication.translate("CFeedPropertiesDlg", u"-", None))
    # retranslateUi

