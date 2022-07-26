from msilib.schema import Error
from PySide2 import QtWidgets, QtCore
from PySide2.QtUiTools import QUiLoader
from fragments_generation import *
from read_db import *

class Branching_Ratios(QtWidgets.QMainWindow):
    signal_dict = QtCore.Signal(list)
    def __init__(self):
        super(Branching_Ratios, self).__init__()
        self.ui = QUiLoader().load('brief sample.ui')
        self.ui.OptionButton.clicked.connect(self.open_options)       
        self.ui.RunButton.clicked.connect(self.show_results)
        self.ui.MoleculeEdit.returnPressed.connect(self.show_results)
        self.ui.comboBox.addItems(['name', 'cas number', 'formula'])
        self.ui.UpdateButton.clicked.connect(self.open_temp)        

    def run(self):
        checked = self.ui.ComputeRatios.isChecked()
        input = self.ui.MoleculeEdit.text()
        text = self.ui.comboBox.currentText()
        if text == 'cas number':
            molecule, cas_exist = translate_cas(input)
            if cas_exist == 0:
                QtWidgets.QMessageBox.critical(self.ui,
                'Error',
                "The input cas number doesn't exist in current data base.")
                raise ValueError("The input cas number doesn't exist in current data base.")
        elif text == 'formula':
            molecule, formula_exist, list_formula = translate_formula(input)
            if formula_exist == 0:
                QtWidgets.QMessageBox.critical(self.ui,
                'Error',
                "The input formula doesn't exist in current data base.")
                raise ValueError("The input formula doesn't exist in current data base.")
            if len(set(list_formula)) > 1:
                QtWidgets.QMessageBox.critical(self.ui,
                'Error',
                "Your input formula exists isomers. Please try more accurate input.")
                raise ValueError("Your input formula exists isomers. Please try more accurate input.")
        else:
            molecule = str(input)

        dict_fragments, dict_mass, dict_peak, total_ratio, molecule_exist, list_basic = connection(molecule)
        if molecule_exist == 0:
            QtWidgets.QMessageBox.critical(self.ui,
                'Error',
                "The input molecule name doesn't exist in current data base.")
            raise ValueError("The input molecule name doesn't exist in current data base.")
        if total_ratio < 0.99:
            QtWidgets.QMessageBox.critical(self.ui,
                'Wrong with Database',
                "The data in database might be imcomplete. Please edit database with 'Option' button.")
        elif total_ratio > 1.01:
            QtWidgets.QMessageBox.critical(self.ui,
                'Wrong with Database',
                "The total of branching ratio is larger than limit(101%). Please edit database with 'Option' button.")
        if checked:
            list_information = [dict_fragments, dict_mass, dict_peak, list_basic]
            return list_information
            
        else:
            QtWidgets.QMessageBox.about(self.ui,
            'Outcomes',
            "Don't forget to tick the check box!")
            raise LookupError("Don't forget to tick the check box!")
    
    def open_options(self):
        data = self.run()
        self.options = Options()
        self.signal_dict.connect(self.options.PrintCurrentData)
        self.signal_dict.emit(data)

    def show_results(self):
        data = self.run()
        self.fragment = show_fragments()
        self.signal_dict.connect(self.fragment.PrintToGui)
        self.signal_dict.emit(data)
        
    def open_temp(self):
        self.identity = identity()


class Options(QtWidgets.QDialog):
    def __init__(self):
        self.ui = QUiLoader().load('Options.ui')
        self.ui.show()
        self.ui.PossibleOptions.setEnabled(False)
        # self.ui.PossibleOptions.clicked.connect(self.confirm_input)
        self.ui.PossibleOptions.clicked.connect(self.upload_input)
        # self.ui.input_table.setColumnWidth(3, 200)
        # self.ui.input_table.setColumnWidth(6, 200)
        self.ui.add_row.clicked.connect(self.add_new_row)
        self.ui.remove_row.clicked.connect(self.remove_new_row)
        self.ui.update_button.clicked.connect(self.update_data)
        self.ui.currentTable.setColumnWidth(3, 200)
        self.ui.currentTable.setColumnWidth(6, 400)

    # def confirm_input(self):
    #     energy_level = str(self.ui.energy_level.text())
    #     if energy_level == '':
    #         QtWidgets.QMessageBox.critical(self.ui,
    #         'Error',
    #         "The energy level input is necessary")
    #         raise ValueError('The energy level input is necessary!')
    #     input_data = []
    #     row_num = self.ui.input_table.rowCount()
    #     for i in range(row_num):
    #         list_input = []
    #         for j in range(8):
    #             input = str(self.ui.input_table.item(i, j))
    #             if input == 'None':
    #                 input = 'nan'
    #             else:
    #                 input = str(self.ui.input_table.item(i, j).text())
    #             list_input.append(input)
    #         input_data.append(tuple(list_input))
    #     self.sql_table(energy_level, input_data)
    #     QtWidgets.QMessageBox.about(self.ui,
    #     'Result',
    #     'Input Confirmed!')
    #     self.ui.close()

    def add_new_row(self):
        self.ui.currentTable.insertRow(0)

    def remove_new_row(self):
        self.ui.currentTable.removeRow(0)

    def update_data(self):
        self.ui.currentTable.update()
        self.ui.PossibleOptions.setEnabled(True)

    # def sql_table(self, energy_level, data):
    #     try:
    #         con = sqlite3.connect("data-20.db")
    #     except sqlite3.Error:
    #         print(sqlite3.Error)
    #     cursor = con.cursor()
    #     cursor.execute(f"""SELECT name from sqlite_master WHERE type = "table" AND name = '{energy_level}'""")
    #     exist_status = cursor.fetchall()
    #     if exist_status == []:
    #         cursor.execute(f"""create table if not exists '{energy_level}'(name text, cas text, formula text, charge_mass_ratio number, peak_height number, branch_ratio number, optional_fragment text)""")
    #         cursor.executemany(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?)""", data)
    #     else:
    #         molecule = data[0][0]
    #         status = self.check_exist(energy_level, molecule)
    #         if status == 0:
    #             cursor.execute(f"""create table if not exists '{energy_level}'(name text, cas text, formula text, charge_mass_ratio number, peak_height number, branch_ratio number, optional_fragment text)""")
    #             cursor.executemany(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?)""", data)
    #         elif status == 1:
    #             for single_row in data:
    #                 charge_mass_ratio = single_row[3]
    #                 peak_height = single_row[4]
    #                 branch_ratio = single_row[5]
    #                 optional_fragment = single_row[6]
    #                 cursor.execute(f"""select * from '{energy_level}' where name = '{molecule}'""")
    #                 check_mass = cursor.fetchall()
    #                 mass_exist = 0
    #                 for sample in check_mass:
    #                     if str(sample[4]) == charge_mass_ratio:
    #                         mass_exist = 1
    #                 if mass_exist == 1:
    #                     cursor.execute(f"""UPDATE '{energy_level}' SET peak_height = '{peak_height}' where name = '{molecule}' AND charge_mass_ratio = '{charge_mass_ratio}'""")
    #                     cursor.execute(f"""UPDATE '{energy_level}' SET branch_ratio = '{branch_ratio}' where name = '{molecule}' AND charge_mass_ratio = '{charge_mass_ratio}'""")
    #                     cursor.execute(f"""UPDATE '{energy_level}' SET optional_fragment = '{optional_fragment}' where name = '{molecule}' AND charge_mass_ratio = '{charge_mass_ratio}'""")
    #                 else:
    #                     cursor.execute(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", single_row)
    #     con.commit()
    #     self.ui.input_table.update()
    #     con.close()

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

    def PrintCurrentData(self, list):
        dict_fragment = list[0]
        dict_mass = list[1]
        dict_peak = list[2]
        list_basic = list[3]
        self.ui.currentTable.setRowCount(len(dict_fragment))
        current_row = 0
        for keys in dict_fragment:
            self.ui.currentTable.setItem(current_row, 0, QtWidgets.QTableWidgetItem(str(list_basic[0])))
            self.ui.currentTable.setItem(current_row, 1, QtWidgets.QTableWidgetItem(str(list_basic[1])))
            self.ui.currentTable.setItem(current_row, 2, QtWidgets.QTableWidgetItem(str(list_basic[2])))
            self.ui.currentTable.setItem(current_row, 4, QtWidgets.QTableWidgetItem(str(dict_peak[keys])))
            self.ui.currentTable.setItem(current_row, 5, QtWidgets.QTableWidgetItem(str(round(float(keys), 7))))
            self.ui.currentTable.setItem(current_row, 6, QtWidgets.QTableWidgetItem(str(dict_fragment[keys])))
            self.ui.currentTable.setItem(current_row, 3, QtWidgets.QTableWidgetItem(str(dict_mass[keys])))
            current_row = current_row + 1
        self.ui.currentTable.update()

    def upload_input(self):
        energy_level = str(self.ui.energy_level.text())
        if energy_level == '':
            QtWidgets.QMessageBox.critical(self.ui,
            'Error',
            "The energy level input is necessary")
            raise ValueError('The energy level input is necessary!')
        input_data = []
        row_num = self.ui.currentTable.rowCount()
        for i in range(row_num):
            list_input = []
            for j in range(7):
                input = str(self.ui.currentTable.item(i, j))
                if input == 'None':
                    input = 'nan'
                else:
                    input = str(self.ui.currentTable.item(i, j).text())
                list_input.append(input)
            input_data.append(tuple(list_input))
        # self.sql_table(energy_level, input_data)
        try:
            con = sqlite3.connect("temp.db")     
        except sqlite3.Error:
            print(sqlite3.Error)
        cursor = con.cursor()
        cursor.execute(f"""create table if not exists '{energy_level}'(name text, cas text, formula text, charge_mass_ratio number, peak_height number, branch_ratio number, optional_fragment text)""")
        cursor.executemany(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?)""", input_data)            
        QtWidgets.QMessageBox.about(self.ui,
        'Result',
        'Input Confirmed!')
        con.commit()
        self.ui.currentTable.update()
        con.close()
        self.ui.close()

class show_fragments(QtWidgets.QDialog):
    def __init__(self):
        super(show_fragments, self).__init__()
        self.ui = QUiLoader().load('show_fragments.ui')
        self.ui.show()
        self.ui.showTable.setColumnWidth(0, 250)
        self.ui.showTable.setColumnWidth(1, 250)
        self.ui.showTable.setColumnWidth(2, 400)

    def PrintToGui(self, list):
        dict_fragment = list[0]
        dict_mass = list[1]
        list_basic = list[3]
        string = f"Molecule: ({list_basic[0]}) Formula: ({list_basic[2]}) Cas number ({list_basic[1]})"
        self.ui.basic_information.setText(string)
        self.ui.showTable.setRowCount(len(dict_fragment))
        current_row = 0
        for keys in dict_fragment:
            self.ui.showTable.setItem(current_row, 0, QtWidgets.QTableWidgetItem(str(round(float(keys), 7))))
            self.ui.showTable.setItem(current_row, 2, QtWidgets.QTableWidgetItem(str(dict_fragment[keys])))
            self.ui.showTable.setItem(current_row, 1, QtWidgets.QTableWidgetItem(str(dict_mass[keys])))
            current_row = current_row + 1
        self.ui.showTable.update()

class show_temp(QtWidgets.QDialog):
    def __init__(self):
        super(show_temp, self).__init__()
        self.ui = QUiLoader().load('double_check.ui')
        self.ui.show()
        try:
            con = sqlite3.connect("temp.db")     
        except sqlite3.Error:
            print(sqlite3.Error)
        cursor = con.cursor()
        sql = """select name from sqlite_master where type='table' order by name"""
        cursor.execute(sql)
        result = cursor.fetchall()
        string = "This temp.db include data for "
        if result == []:
            string = "The temp.db is currently empty."
        else:
            for i in range(len(result)):
                string = string + f"({result[i]})"
                self.ui.energyOption.addItem(str(result[i]))
        self.ui.label.setText(string)
        self.ui.LoadButton.clicked.connect(self.PrintTemp)
        self.ui.submitTable.clicked.connect(self.submitToBase)
        self.ui.showTable.setColumnWidth(3, 250)
        self.ui.showTable.setColumnWidth(5, 300)
        self.ui.showTable.setColumnWidth(6, 400)
        self.ui.delLine.clicked.connect(self.deleteLine)
        self.ui.delTable.clicked.connect(self.deleteTable)
        con.close()

    def PrintTemp(self):
        con = sqlite3.connect("temp.db")
        cursor = con.cursor()
        energy_level = self.ui.energyOption.currentText()
        energy_level = energy_level[1:-2]
        sql = f"""select * from {energy_level}"""
        cursor.execute(sql)
        list = cursor.fetchall()
        self.ui.showTable.setRowCount(len(list))
        current_row = 0
        for row in list:
            self.ui.showTable.setItem(current_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.showTable.setItem(current_row, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.showTable.setItem(current_row, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.showTable.setItem(current_row, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.showTable.setItem(current_row, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.ui.showTable.setItem(current_row, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            self.ui.showTable.setItem(current_row, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            current_row = current_row + 1
        self.ui.showTable.update()
        con.close()

    def sql_table(self, energy_level, data):
        try:
            con = sqlite3.connect("data-20.db")
        except sqlite3.Error:
            print(sqlite3.Error)
        cursor = con.cursor()
        cursor.execute(f"""SELECT name from sqlite_master WHERE type = "table" AND name = '{energy_level}'""")
        exist_status = cursor.fetchall()
        if exist_status == []:
            cursor.execute(f"""create table if not exists '{energy_level}'(name text, cas text, formula text, charge_mass_ratio number, peak_height number, branch_ratio number, optional_fragment text)""")
            cursor.executemany(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?)""", data)
        else:
            molecule = data[0][0]
            status = self.check_exist(energy_level, molecule)
            if status == 0:
                cursor.execute(f"""create table if not exists '{energy_level}'(name text, cas text, formula text, charge_mass_ratio number, peak_height number, branch_ratio number, optional_fragment text)""")
                cursor.executemany(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?)""", data)
            elif status == 1:
                for single_row in data:
                    charge_mass_ratio = single_row[3]
                    peak_height = single_row[4]
                    branch_ratio = single_row[5]
                    optional_fragment = single_row[6]
                    cursor.execute(f"""select * from '{energy_level}' where name = '{molecule}'""")
                    check_mass = cursor.fetchall()
                    mass_exist = 0
                    for sample in check_mass:
                        if str(sample[3]) == charge_mass_ratio:
                            mass_exist = 1
                    if mass_exist == 1:
                        cursor.execute(f"""UPDATE '{energy_level}' SET peak_height = '{peak_height}' where name = '{molecule}' AND charge_mass_ratio = '{charge_mass_ratio}'""")
                        cursor.execute(f"""UPDATE '{energy_level}' SET branch_ratio = '{branch_ratio}' where name = '{molecule}' AND charge_mass_ratio = '{charge_mass_ratio}'""")
                        cursor.execute(f"""UPDATE '{energy_level}' SET optional_fragment = '{optional_fragment}' where name = '{molecule}' AND charge_mass_ratio = '{charge_mass_ratio}'""")
                    else:
                        cursor.execute(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?)""", single_row)
        con.commit()
        self.ui.showTable.update()
        con.close()

    def submitToBase(self):
        energy_level = self.ui.energyOption.currentText()
        energy_level = str(energy_level[2:-3])
        input_data = []
        row_num = self.ui.showTable.rowCount()
        for i in range(row_num):
            list_input = []
            for j in range(7):
                input = str(self.ui.showTable.item(i, j).text())
                list_input.append(input)
            input_data.append(tuple(list_input))
        self.sql_table(energy_level, input_data)
        QtWidgets.QMessageBox.about(self.ui,
        'Result',
        'Upload successful!')
        conn = sqlite3.connect('temp.db')
        cursor_2 = conn.cursor()
        cursor_2.execute(f"DROP table if exists '{energy_level}'")
        self.ui.close()
    
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

    def deleteLine(self):
        currentRow = self.ui.showTable.currentRow()
        self.ui.showTable.removeRow(currentRow)

    def deleteTable(self):
        energy_level = self.ui.energyOption.currentText()
        energy_level = str(energy_level[2:-3])
        con = sqlite3.connect('temp.db')
        cursor = con.cursor()
        cursor.execute(f"DROP table if exists '{energy_level}'")
        con.close()

class identity(QtWidgets.QWidget):
    def __init__(self):
        super(identity, self).__init__()
        self.ui = QUiLoader().load('identity.ui')
        self.ui.show()
        self.ui.OkButton.clicked.connect(self.clickOk)
        self.ui.CancelButton.clicked.connect(self.ui.close)
    
    def clickOk(self):
        text = self.ui.Input.text()
        if text == 'London':
            self.temp = show_temp()
        else:
            QtWidgets.QMessageBox.about(self.ui,
                'Result',
                'Access denied!')
        self.ui.close()
    
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
app = QtWidgets.QApplication([])
PICS = Branching_Ratios()
PICS.ui.show()
app.exec_()