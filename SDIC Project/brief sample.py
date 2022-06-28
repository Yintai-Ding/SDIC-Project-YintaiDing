from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader

class Branching_Ratios(QtWidgets.QMainWindow):
    def __init__(self):
        self.ui = QUiLoader().load('brief sample.ui')
        self.ui.OptionButton.clicked.connect(self.open_options)
        # self.ui.ComputeRatios.clicked.connect(self.status_check)        
        self.ui.RunButton.clicked.connect(self.run)
        self.ui.MoleculeEdit.returnPressed.connect(self.run)
    
    def run(self):
        checked = self.ui.ComputeRatios.isChecked()
        molecule = self.ui.MoleculeEdit.text()
        # self.dlg = Options()
        # text = self.dlg.InputInformation.toPlainText()
        # print(text_experimental)
        if checked:
            QMessageBox.about(self.ui,
            'Outcomes',
            f'''Your chosen molecule is: \n{molecule}\nHere is your simulation results!''')
        else:
            QMessageBox.about(self.ui,
            'Outcomes',
            "Don't forget to choose options!")
    
    def open_options(self):
        self.dlg = Options()
        # print('789')#Debug
        # text_experimental = self.dlg.InputInformation.toPlainText()
        # print(text_experimental)
        # return text_experimental

class Options(QtWidgets.QDialog):
    def __init__(self):
        self.ui = QUiLoader().load('Options.ui')
        self.ui.show()
        # text_experimental = self.ui.InputInformation.toPlainText()
        self.ui.PossibleOptions.clicked.connect(self.confirm_input)

    def confirm_input(self):
        # print('message confirmed!')#Debug
        text_experimental = self.ui.InputInformation.toPlainText()
        print(text_experimental)
        QMessageBox.about(self.ui,
        'Result',
        'Input Confirmed!')
        # print(text_experimental)
        self.ui.close()

app = QApplication([])
PICS = Branching_Ratios()
PICS.ui.show()
app.exec_()