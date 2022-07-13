from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from fragments_generation import *
from read_db import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtCore import *

class Branching_Ratios(QtWidgets.QMainWindow):
    signal_1 = Signal(str)
    def __init__(self):
        super(Branching_Ratios, self).__init__()
        self.ui = QUiLoader().load('brief sample.ui')
        self.ui.OptionButton.clicked.connect(self.open_options)
        # self.ui.ComputeRatios.clicked.connect(self.status_check)        
        self.ui.RunButton.clicked.connect(self.run)
        self.ui.MoleculeEdit.returnPressed.connect(self.run)
        self.ui.comboBox.addItems(['name', 'cas number', 'formula'])
        

    def run(self):
        checked = self.ui.ComputeRatios.isChecked()
        input = self.ui.MoleculeEdit.text()
        text = self.ui.comboBox.currentText()
        # self.dlg = Options()
        # text = self.dlg.InputInformation.toPlainText()
        # print(text_experimental)
        if text == 'cas number':
            molecule = translate_cas(input)
        elif text == 'formula':
            molecule = translate_formula(input)
        else:
            molecule = str(input)

        dict_fragments, dict_mass, total_ratio = connection(molecule)
        if checked:
            self.fragment = show_fragments()
            self.signal_1.connect(self.fragment.PrintToGui)
            self.signal_1.emit(self.chart(dict_fragments, dict_mass))
            
        # dict_LF = np.load('processed_data.npy', allow_pickle = True).item()
        # formula = dict_LF[molecule]['formula'].replace(" ", "")
        # fragments = dict_LF[molecule]['optional_fragments']
        # test = Generation(formula.lower())
        # list, dict = test.fragments()
        # list_LF = []
        # for fragment in fragments:
        #     for things in fragment:
        #         list_LF.append(things)
        # list_YT = []
        # for fragment in dict.values():
        #     for things in fragment:
        #         list_YT.append(things)
        # intersection = set(list_LF).intersection(set(list_YT))
        # difference_YT = set(list_YT).difference(set(list_LF))
        # difference_LF = set(list_LF).difference(set(list_YT))
        # if checked:
        #     QMessageBox.about(self.ui,
        #     'Outcomes',
        #     f'''Your chosen molecule is: \n{molecule}\nHere is your simulation results!\n{intersection}\nMissing fragments: \n{difference_YT}\nUnexpected fragments: \n{difference_LF}''')
        else:
            QMessageBox.about(self.ui,
            'Outcomes',
            "Don't forget to choose options!")
    
    def open_options(self):
        self.dlg = Options()
        # text_experimental = self.dlg.InputInformation.toPlainText()
        # print(text_experimental)
        # return text_experimental

    def chart(self, dict, dict_mass):
        string = 'Branching Ratio:      Charge_Mass Ratio:    Possible Fragments: \n'
        for keys in dict:
            string = string + f'''{round(float(keys), 7)}: \t\t\t{dict_mass[keys]}\t\t\t{dict[keys]}\n'''
        return string

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

class show_fragments(QtWidgets.QDialog):
    def __init__(self):
        super(show_fragments, self).__init__()
        self.ui = QUiLoader().load('show_fragments.ui')
        self.ui.show()

    def PrintToGui(self, text):
        self.ui.textBrowser.setPlainText(str(text))


app = QApplication([])
PICS = Branching_Ratios()
PICS.ui.show()
app.exec_()