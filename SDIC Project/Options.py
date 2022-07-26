# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Options.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Options(object):
    def setupUi(self, Options):
        if not Options.objectName():
            Options.setObjectName(u"Options")
        Options.resize(400, 300)
        self.verticalLayout_2 = QVBoxLayout(Options)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.InputInformation = QPlainTextEdit(Options)
        self.InputInformation.setObjectName(u"InputInformation")

        self.verticalLayout.addWidget(self.InputInformation)

        self.PossibleOptions = QPushButton(Options)
        self.PossibleOptions.setObjectName(u"PossibleOptions")

        self.verticalLayout.addWidget(self.PossibleOptions)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Options)

        QMetaObject.connectSlotsByName(Options)
    # setupUi

    def retranslateUi(self, Options):
        Options.setWindowTitle(QCoreApplication.translate("Options", u"Options", None))
        self.InputInformation.setPlaceholderText(QCoreApplication.translate("Options", u"Please input your experimental data", None))
        self.PossibleOptions.setText(QCoreApplication.translate("Options", u"Possible Options", None))
    # retranslateUi

