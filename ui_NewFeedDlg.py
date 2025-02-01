# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NewFeedDlg.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

class Ui_NewFeedDlg(object):
    def setupUi(self, NewFeedDlg):
        if not NewFeedDlg.objectName():
            NewFeedDlg.setObjectName(u"NewFeedDlg")
        NewFeedDlg.resize(611, 221)
        icon = QIcon()
        icon.addFile(u"Resources/RssReader.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        NewFeedDlg.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(NewFeedDlg)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.stackedWidget = QStackedWidget(NewFeedDlg)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setAutoFillBackground(False)
        self.stackedWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_2 = QVBoxLayout(self.page)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.page)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_2)

        self.feedUrlEdit = QLineEdit(self.page)
        self.feedUrlEdit.setObjectName(u"feedUrlEdit")

        self.horizontalLayout.addWidget(self.feedUrlEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_3 = QVBoxLayout(self.page_2)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.feedNameLabel = QLabel(self.page_2)
        self.feedNameLabel.setObjectName(u"feedNameLabel")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.feedNameLabel.setFont(font)

        self.verticalLayout_3.addWidget(self.feedNameLabel)

        self.feedUrlLabel = QLabel(self.page_2)
        self.feedUrlLabel.setObjectName(u"feedUrlLabel")

        self.verticalLayout_3.addWidget(self.feedUrlLabel)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.descriptionLabel = QLabel(self.page_2)
        self.descriptionLabel.setObjectName(u"descriptionLabel")
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setTextInteractionFlags(Qt.NoTextInteraction)

        self.verticalLayout_3.addWidget(self.descriptionLabel)

        self.verticalSpacer_2 = QSpacerItem(20, 47, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)

        self.line = QFrame(NewFeedDlg)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.nextButton = QPushButton(NewFeedDlg)
        self.nextButton.setObjectName(u"nextButton")

        self.horizontalLayout_2.addWidget(self.nextButton)

        self.cancelButton = QPushButton(NewFeedDlg)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_2.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(NewFeedDlg)
        self.cancelButton.clicked.connect(NewFeedDlg.reject)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(NewFeedDlg)
    # setupUi

    def retranslateUi(self, NewFeedDlg):
        NewFeedDlg.setWindowTitle(QCoreApplication.translate("NewFeedDlg", u"New Feed", None))
        self.label_2.setText(QCoreApplication.translate("NewFeedDlg", u"Feed URL", None))
        self.feedNameLabel.setText(QCoreApplication.translate("NewFeedDlg", u"-", None))
        self.feedUrlLabel.setText(QCoreApplication.translate("NewFeedDlg", u"-", None))
        self.descriptionLabel.setText(QCoreApplication.translate("NewFeedDlg", u"-", None))
        self.nextButton.setText(QCoreApplication.translate("NewFeedDlg", u"Next >", None))
        self.cancelButton.setText(QCoreApplication.translate("NewFeedDlg", u"Cancel", None))
    # retranslateUi

