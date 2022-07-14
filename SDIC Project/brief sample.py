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
        self.ui.RunButton.clicked.connect(self.run)
        self.ui.MoleculeEdit.returnPressed.connect(self.run)
        self.ui.comboBox.addItems(['name', 'cas number', 'formula'])
        

    def run(self):
        checked = self.ui.ComputeRatios.isChecked()
        input = self.ui.MoleculeEdit.text()
        text = self.ui.comboBox.currentText()
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
        self.ui.input_table.setColumnWidth(2, 250)
        self.ui.input_table.setColumnWidth(4, 200)
        self.ui.input_table.setColumnWidth(7, 200)
        self.ui.add_row.clicked.connect(self.add_new_row)
        self.ui.remove_row.clicked.connect(self.remove_new_row)
        self.ui.update_button.clicked.connect(self.update_data)

    def confirm_input(self):
        energy_level = str(self.ui.energy_level.text())
        input_data = []
        row_num = self.ui.input_table.rowCount()
        for i in range(row_num):
            list_input = []
            for j in range(8):
                input = str(self.ui.input_table.item(i, j))
                if input == 'None':
                    input = 'NULL'
                else:
                    input = str(self.ui.input_table.item(i, j).text())
                list_input.append(input)
            input_data.append(tuple(list_input))
        self.sql_table(energy_level, input_data)
        QMessageBox.about(self.ui,
        'Result',
        'Input Confirmed!')
        self.ui.close()

    def add_new_row(self):
        self.ui.input_table.insertRow(0)

    def remove_new_row(self):
        self.ui.input_table.removeRow(0)

    def update_data(self):
        self.ui.input_table.update()

    def sql_table(self, energy_level, data):
        try:
            con = sqlite3.connect("data-20.db")
        except sqlite3.Error:
            print(sqlite3.Error)
        cursor = con.cursor()
        cursor.execute(f"""SELECT name from sqlite_master WHERE type = "table" AND name = '{energy_level}'""")
        exist_status = cursor.fetchall()
        if exist_status == []:
            cursor.execute(f"""create table if not exists '{energy_level}'(name text, cas text, nist_mass_spec_num text, formula text, charge_mass_ratio number, peak_height number, branch_ratio number, optional_fragment text)""")
            cursor.executemany(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", data)
        else:
            molecule = data[0][0]
            status = self.check_exist(energy_level, molecule)
            if status == 0:
                cursor.execute(f"""create table if not exists '{energy_level}'(name text, cas text, nist_mass_spec_num text, formula text, charge_mass_ratio number, peak_height number, branch_ratio number, optional_fragment text)""")
                cursor.executemany(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", data)
            elif status == 1:
                for single_row in data:
                    charge_mass_ratio = single_row[4]
                    peak_height = single_row[5]
                    branch_ratio = single_row[6]
                    optional_fragment = single_row[7]
                    cursor.execute(f"""select * from '{energy_level}' where name = '{molecule}'""")
                    check_mass = cursor.fetchall()
                    mass_exist = 0
                    for sample in check_mass:
                        if str(sample[4]) == charge_mass_ratio:
                            mass_exist = 1
                    if mass_exist == 1:
                        cursor.execute(f"""UPDATE '{energy_level}' SET peak_height = '{peak_height}' where name = '{molecule}' AND charge_mass_ratio = '{charge_mass_ratio}'""")
                        cursor.execute(f"""UPDATE '{energy_level}' SET branch_ratio = '{branch_ratio}' where name = '{molecule}' AND charge_mass_ratio = '{charge_mass_ratio}'""")
                        cursor.execute(f"""UPDATE '{energy_level}' SET optional_fragment = '{optional_fragment}' where name = '{molecule}' AND charge_mass_ratio = '{charge_mass_ratio}'""")
                    else:
                        cursor.execute(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", single_row)
        con.commit()
        self.ui.input_table.update()
        con.close()

    def check_exist(self, energy_level, molcule):
        conn = sqlite3.connect("data-20.db")
        cursor = conn.cursor()
        sql = f"""select * from '{energy_level}'"""
        cursor.execute(sql)
        result = cursor.fetchall()
        status = 0
        for from_db in result:
            if from_db[0] == molcule:
                status = 1
        conn.close()
        return status

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