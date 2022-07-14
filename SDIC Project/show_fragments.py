# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'show_fragments.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_show_fragments(object):
    def setupUi(self, show_fragments):
        if not show_fragments.objectName():
            show_fragments.setObjectName(u"show_fragments")
        show_fragments.setEnabled(True)
        show_fragments.resize(2000, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(show_fragments.sizePolicy().hasHeightForWidth())
        show_fragments.setSizePolicy(sizePolicy)
        show_fragments.setMinimumSize(QSize(2000, 500))
        self.verticalLayout_2 = QVBoxLayout(show_fragments)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(show_fragments)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamily(u"Calibri")
        font.setPointSize(15)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.textBrowser = QTextBrowser(show_fragments)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setFont(font)

        self.verticalLayout.addWidget(self.textBrowser)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(show_fragments)

        QMetaObject.connectSlotsByName(show_fragments)
    # setupUi

    def retranslateUi(self, show_fragments):
        show_fragments.setWindowTitle(QCoreApplication.translate("show_fragments", u"Show Fragments", None))
        self.label.setText(QCoreApplication.translate("show_fragments", u"Here is the possible fragments and branching ratios:", None))
    # retranslateUi

