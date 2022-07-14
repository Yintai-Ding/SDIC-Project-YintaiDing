# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'brief sample.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_BranchingRatios(object):
    def setupUi(self, BranchingRatios):
        if not BranchingRatios.objectName():
            BranchingRatios.setObjectName(u"BranchingRatios")
        BranchingRatios.resize(1000, 500)
        BranchingRatios.setMinimumSize(QSize(1000, 500))
        self.centralwidget = QWidget(BranchingRatios)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        font = QFont()
        font.setFamily(u"Calibri")
        font.setPointSize(15)
        self.comboBox.setFont(font)
        self.comboBox.setEditable(False)
        self.comboBox.setMaxVisibleItems(10)
        self.comboBox.setMaxCount(2147483645)

        self.horizontalLayout.addWidget(self.comboBox)

        self.MoleculeEdit = QLineEdit(self.centralwidget)
        self.MoleculeEdit.setObjectName(u"MoleculeEdit")
        self.MoleculeEdit.setMinimumSize(QSize(0, 0))
        self.MoleculeEdit.setFont(font)

        self.horizontalLayout.addWidget(self.MoleculeEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.CheckBoxLayout = QHBoxLayout()
        self.CheckBoxLayout.setObjectName(u"CheckBoxLayout")
        self.ComputeRatios = QCheckBox(self.centralwidget)
        self.ComputeRatios.setObjectName(u"ComputeRatios")
        self.ComputeRatios.setFont(font)

        self.CheckBoxLayout.addWidget(self.ComputeRatios)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.CheckBoxLayout.addItem(self.horizontalSpacer)

        self.OptionButton = QPushButton(self.centralwidget)
        self.OptionButton.setObjectName(u"OptionButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OptionButton.sizePolicy().hasHeightForWidth())
        self.OptionButton.setSizePolicy(sizePolicy)
        self.OptionButton.setFont(font)

        self.CheckBoxLayout.addWidget(self.OptionButton)


        self.verticalLayout.addLayout(self.CheckBoxLayout)

        self.RunButtonLayout = QHBoxLayout()
        self.RunButtonLayout.setObjectName(u"RunButtonLayout")
        self.RunButtonLayout.setContentsMargins(0, 100, -1, -1)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.RunButtonLayout.addItem(self.horizontalSpacer_2)

        self.RunButton = QPushButton(self.centralwidget)
        self.RunButton.setObjectName(u"RunButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.RunButton.sizePolicy().hasHeightForWidth())
        self.RunButton.setSizePolicy(sizePolicy1)
        self.RunButton.setFont(font)

        self.RunButtonLayout.addWidget(self.RunButton)


        self.verticalLayout.addLayout(self.RunButtonLayout)

        BranchingRatios.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(BranchingRatios)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 22))
        BranchingRatios.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(BranchingRatios)
        self.statusbar.setObjectName(u"statusbar")
        BranchingRatios.setStatusBar(self.statusbar)

        self.retranslateUi(BranchingRatios)

        QMetaObject.connectSlotsByName(BranchingRatios)
    # setupUi

    def retranslateUi(self, BranchingRatios):
        BranchingRatios.setWindowTitle(QCoreApplication.translate("BranchingRatios", u"Branching Ratios", None))
        self.comboBox.setCurrentText("")
        self.comboBox.setPlaceholderText("")
        self.MoleculeEdit.setPlaceholderText(QCoreApplication.translate("BranchingRatios", u"Please input the information of molecule", None))
        self.ComputeRatios.setText(QCoreApplication.translate("BranchingRatios", u"Calculate branching ratios for all possible fragments", None))
        self.OptionButton.setText(QCoreApplication.translate("BranchingRatios", u"Options", None))
        self.RunButton.setText(QCoreApplication.translate("BranchingRatios", u"Run", None))
    # retranslateUi

