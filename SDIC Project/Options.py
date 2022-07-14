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
        Options.resize(1000, 800)
        Options.setMinimumSize(QSize(1000, 400))
        self.verticalLayout_2 = QVBoxLayout(Options)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.energy_level = QLineEdit(Options)
        self.energy_level.setObjectName(u"energy_level")
        font = QFont()
        font.setFamily(u"Calibri")
        font.setPointSize(12)
        self.energy_level.setFont(font)

        self.verticalLayout.addWidget(self.energy_level)

        self.input_table = QTableWidget(Options)
        if (self.input_table.columnCount() < 8):
            self.input_table.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.input_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.input_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.input_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.input_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.input_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.input_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.input_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.input_table.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        if (self.input_table.rowCount() < 1):
            self.input_table.setRowCount(1)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.input_table.setVerticalHeaderItem(0, __qtablewidgetitem8)
        self.input_table.setObjectName(u"input_table")
        self.input_table.setEnabled(True)
        self.input_table.horizontalHeader().setProperty("showSortIndicator", True)
        self.input_table.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.input_table)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.add_row = QPushButton(Options)
        self.add_row.setObjectName(u"add_row")
        self.add_row.setFont(font)

        self.horizontalLayout.addWidget(self.add_row)

        self.remove_row = QPushButton(Options)
        self.remove_row.setObjectName(u"remove_row")
        self.remove_row.setFont(font)

        self.horizontalLayout.addWidget(self.remove_row)

        self.update_button = QPushButton(Options)
        self.update_button.setObjectName(u"update_button")
        self.update_button.setFont(font)

        self.horizontalLayout.addWidget(self.update_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.PossibleOptions = QPushButton(Options)
        self.PossibleOptions.setObjectName(u"PossibleOptions")
        self.PossibleOptions.setFont(font)

        self.verticalLayout.addWidget(self.PossibleOptions)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Options)

        QMetaObject.connectSlotsByName(Options)
    # setupUi

    def retranslateUi(self, Options):
        Options.setWindowTitle(QCoreApplication.translate("Options", u"Options", None))
        self.energy_level.setText("")
        self.energy_level.setPlaceholderText(QCoreApplication.translate("Options", u"Please input the electron energy level of your data!  e.g. please input 'eighty' for 80eV", None))
        ___qtablewidgetitem = self.input_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Options", u"name", None));
        ___qtablewidgetitem1 = self.input_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Options", u"cas number", None));
        ___qtablewidgetitem2 = self.input_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Options", u"nist_mass_spec_number", None));
        ___qtablewidgetitem3 = self.input_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Options", u"formula", None));
        ___qtablewidgetitem4 = self.input_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Options", u"charge-mass ratio", None));
        ___qtablewidgetitem5 = self.input_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Options", u"peak height", None));
        ___qtablewidgetitem6 = self.input_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Options", u"branch ratio", None));
        ___qtablewidgetitem7 = self.input_table.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Options", u"possible fragments", None));
        self.add_row.setText(QCoreApplication.translate("Options", u"Add Row", None))
        self.remove_row.setText(QCoreApplication.translate("Options", u"Remove Row", None))
        self.update_button.setText(QCoreApplication.translate("Options", u"Update", None))
        self.PossibleOptions.setText(QCoreApplication.translate("Options", u"Submit Experimental Data", None))
    # retranslateUi

