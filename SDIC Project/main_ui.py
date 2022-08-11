from PySide2 import QtWidgets, QtCore
from PySide2.QtUiTools import QUiLoader
from fragments_generation import *
from read_db import *

class Branching_Ratios(QtWidgets.QMainWindow):
    '''This is the main window of the GUI. It will accept user's input of name, CAS number and formula of molecule'''
    signal_dict = QtCore.Signal(list)# this signal will send list of data to Option and Show_fragments page
    def __init__(self):
        super(Branching_Ratios, self).__init__()
        self.ui = QUiLoader().load('main_ui.ui')
        self.ui.OptionButton.clicked.connect(self.open_options)       
        self.ui.RunButton.clicked.connect(self.show_results)
        self.ui.MoleculeEdit.returnPressed.connect(self.show_results)
        self.ui.comboBox.addItems(['name', 'cas number', 'formula'])
        self.ui.UpdateButton.clicked.connect(self.open_temp)    
        self.ui.editTICS.clicked.connect(self.open_TICS)
        self.ui.label_isomer.setEnabled(False)
        self.ui.comboBox_isomer.setEnabled(False)# this widget will be enabled when isomers exist for formula input    

    def run(self):
        '''Firstly check the status of user input and build connection to database'''
        checked = self.ui.ComputeRatios.isChecked()
        input = self.ui.MoleculeEdit.text()
        text = self.ui.comboBox.currentText()
        isomer_choice = self.ui.comboBox_isomer.currentText()
        if isomer_choice != '' and isomer_choice != 'Not isomers':
            input = isomer_choice
            text = 'name'
        elif isomer_choice == 'Not isomers':# User wish to try another input
            self.ui.comboBox_isomer.clear()
            self.ui.comboBox_isomer.setEnabled(False)
        if text == 'cas number':# some CAS number is empty in current database
            molecule, cas_exist = translate_cas(input)
            if cas_exist == 0:
                QtWidgets.QMessageBox.critical(self.ui,
                'Error',
                "The input cas number doesn't exist in current data base.")
                raise ValueError("The input cas number doesn't exist in current data base.")
        elif text == 'formula':# some formulas exist isomers and should send a message to users
            molecule, formula_exist, list_formula = translate_formula(input)
            if formula_exist == 0:
                QtWidgets.QMessageBox.critical(self.ui,
                'Error',
                "The input formula doesn't exist in current data base.")
                raise ValueError("The input formula doesn't exist in current data base.")
            if len(set(list_formula)) > 1:# when the input formula exists isomers, GUI will print out the name of isomers
                QtWidgets.QMessageBox.critical(self.ui,
                'Error',
                f"Your input formula exists isomers.\n({set(list_formula)}) \nPlease try more accurate input.")
                self.ui.label_isomer.setEnabled(True)
                self.ui.comboBox_isomer.setEnabled(True)
                self.ui.comboBox_isomer.addItem('Not isomers')
                for isomer in set(list_formula):# add isomers to combo box for further choices
                    self.ui.comboBox_isomer.addItem(isomer)
                raise ValueError("Your input formula exists isomers. Please try more accurate input.")
        else:
            molecule = str(input)

        dict_fragments, dict_mass, dict_peak, total_ratio, molecule_exist, list_basic = connection(molecule)
        if molecule_exist == 0:# check if the name of molecule exist in current database
            QtWidgets.QMessageBox.critical(self.ui,
                'Error',
                "The input molecule name doesn't exist in current data base.")
        else: 
            if round(total_ratio, 5) < 1:# check if the branching ratio is sum up to 1
                QtWidgets.QMessageBox.critical(self.ui,
                    'Wrong with Database',
                    "The data in database might be imcomplete. Please edit database with 'Option' button.")
            elif round(total_ratio, 5) > 1:# Here the round up digit is set to 5. This could be rised if necessary.
                QtWidgets.QMessageBox.critical(self.ui,
                    'Wrong with Database',
                    "The total of branching ratio is larger than limit(100%). Please edit database with 'Option' button.")
        if checked:
            list_information = [dict_fragments, dict_mass, dict_peak, list_basic]
            return list_information
            
        else:
            QtWidgets.QMessageBox.about(self.ui,
            'Outcomes',
            "Don't forget to tick the check box!")
            raise LookupError("Don't forget to tick the check box!")
    
    def open_options(self):
        '''Initialize Options class and send same signal to class'''
        data = self.run()
        self.options = Options()
        self.signal_dict.connect(self.options.PrintCurrentData)
        self.signal_dict.emit(data)

    def show_results(self):
        '''Initialize show_fragments class and send signal to class'''
        data = self.run()
        self.fragment = show_fragments()
        self.signal_dict.connect(self.fragment.PrintToGui)
        self.signal_dict.emit(data)
        
    def open_temp(self):
        self.identity = identity()

    def open_TICS(self):
        data = self.run()
        self.TICS = EditTICS()
        self.signal_dict.connect(self.TICS.PrintTICS)
        self.signal_dict.emit(data)

class Options(QtWidgets.QDialog):
    '''This is a option widget that allow users to input missing data or edit current data. The input will be saved in a temporary database.'''
    def __init__(self):
        self.ui = QUiLoader().load('Options.ui')
        self.ui.show()
        self.ui.PossibleOptions.setEnabled(False)
        self.ui.PossibleOptions.clicked.connect(self.upload_input)
        self.ui.add_row.clicked.connect(self.add_new_row)
        self.ui.remove_row.clicked.connect(self.remove_new_row)
        self.ui.update_button.clicked.connect(self.update_data)
        self.ui.currentTable.setColumnWidth(3, 200)
        self.ui.currentTable.setColumnWidth(6, 400)

    def add_new_row(self):
        self.ui.currentTable.insertRow(0)
        self.ui.currentTable.setItem(0, 0, QtWidgets.QTableWidgetItem(str(self.ui.currentTable.item(1, 0).text())))
        self.ui.currentTable.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.ui.currentTable.item(1, 1).text())))

    def remove_new_row(self):
        currentRow = self.ui.currentTable.currentRow()
        self.ui.currentTable.removeRow(currentRow)

    def update_data(self):
        '''This will update the branching ratios in table and prepare for upload.'''
        self.ui.currentTable.update()
        self.ui.PossibleOptions.setEnabled(True)
        list_peak = []
        total_peak = 0
        total_row = self.ui.currentTable.rowCount()
        for i in range(total_row):
            list_peak.append(self.ui.currentTable.item(i, 4).text())
            total_peak = total_peak + int(self.ui.currentTable.item(i, 4).text())
        for j in range(total_row):
            branching_ratio = int(list_peak[j]) / total_peak
            self.ui.currentTable.setItem(j, 5, QtWidgets.QTableWidgetItem(str(branching_ratio)))

    def PrintCurrentData(self, list):
        '''Print the current data in database to a table and allow users to edit directly'''
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
        '''The users' input will not save in database directly. These will be upload to a temporary database names "temp.db"'''
        energy_level = str(self.ui.energy_level.text())
        if energy_level == '':
            QtWidgets.QMessageBox.critical(self.ui,
            'Error',
            "The energy level input is necessary")
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
        total_ratio = 0
        for single_data in input_data:
            total_ratio = total_ratio + float(single_data[5])
        if round(total_ratio, 7) != 1:# double check if the total ratio is 1
            QtWidgets.QMessageBox.critical(self.ui,
            'Error',
            "The current total ratio doesn't sum up to 1!")
            raise ValueError("The current total ratio doesn't sum up to 1!")
        try: # build connection with the temporary database 
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
    '''This widget shows the possible fragments and branching ratio from database.'''
    def __init__(self):
        super(show_fragments, self).__init__()
        self.ui = QUiLoader().load('show_fragments.ui')
        self.ui.show()
        self.ui.showTable.setColumnWidth(0, 250)
        self.ui.showTable.setColumnWidth(1, 250)
        self.ui.showTable.setColumnWidth(2, 400)
        self.ui.showTable.setColumnWidth(3, 400)

    def PrintToGui(self, list):
        '''Print the current data to a table on screen'''
        dict_fragment = list[0]
        dict_mass = list[1]
        list_basic = list[3]
        cross_section = self.PrintPartial(list_basic[0], 70)
        string = f"Molecule: ({list_basic[0]}) Formula: ({list_basic[2]}) Cas number ({list_basic[1]})"
        self.ui.basic_information.setText(string)
        self.ui.showTable.setRowCount(len(dict_fragment))
        current_row = 0
        for keys in dict_fragment:
            self.ui.showTable.setItem(current_row, 0, QtWidgets.QTableWidgetItem(str(round(float(keys), 7))))
            # round the branching ratio to 7 digits 
            self.ui.showTable.setItem(current_row, 2, QtWidgets.QTableWidgetItem(str(dict_fragment[keys])))
            self.ui.showTable.setItem(current_row, 1, QtWidgets.QTableWidgetItem(str(dict_mass[keys])))
            if cross_section == "":
                partial_cross_section = "No partial ionization cross section data found."
            else:
                partial_cross_section = round(float(keys) * float(cross_section), 7)
            self.ui.showTable.setItem(current_row, 3, QtWidgets.QTableWidgetItem(str(partial_cross_section)))
            current_row = current_row + 1
        self.ui.showTable.update()
        self.PrintPossible(list_basic[0])

    def PrintPartial(self, molecule, energy_level):
        con_p = sqlite3.connect('data-20.db')
        cursor_p = con_p.cursor()
        sql = """select * from 'energy_vs_total_beb'"""
        cursor_p.execute(sql)
        result = cursor_p.fetchall()
        cross_section = ""
        for total_beb in result:
            if total_beb[0] == molecule and total_beb[2] == energy_level:
                cross_section = total_beb[3]
        return cross_section

    def PrintPossible(self, molecule):
        '''Load fragments of molecule from database and generated from functions. Make comparison and check missing fragments'''
        molecule_bond = Generation(molecule)
        list_bond = molecule_bond.fragments()
        if list_bond == []:# The data for relative position of atoms is limited. Only 30 molecules.
            self.ui.other_possible.append("Currently no possible missing fragment could be proved as exist.")
        else:
            conn = sqlite3.connect("data-20.db")
            cursor = conn.cursor()
            sql = """select * from 'main_data'"""
            cursor.execute(sql)
            result = cursor.fetchall()
            list_data = []
            for row in result:
                if row[0] == molecule:
                    list_data.extend(row[6].split(','))
            difference_bond = set(list_bond).difference(set(list_data))# check the difference
            self.ui.other_possible.append(f"Possible missing fragments in database: {difference_bond}")
            conn.close()

class show_temp(QtWidgets.QDialog):
    '''Load the user-upload data from temporary database and make double check by members'''
    def __init__(self):
        super(show_temp, self).__init__()
        self.ui = QUiLoader().load('double_check.ui')
        self.ui.show()
        try:
            con = sqlite3.connect("temp.db")# build connection to temporary database     
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
        '''Print out the data with energy level'''
        con = sqlite3.connect("temp.db")
        cursor = con.cursor()
        energy_level = self.ui.energyOption.currentText()
        energy_level = energy_level[1:-2]
        sql = f"""select * from {energy_level}"""
        cursor.execute(sql)# select table with chosen energy level
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
        '''Merge the uploaded data with current database'''
        try:
            con = sqlite3.connect("data-20.db")
        except sqlite3.Error:
            print(sqlite3.Error)
        cursor = con.cursor()
        if energy_level == '70 eV':
            energy_level = 'main_data'
        cursor.execute(f"""SELECT name from sqlite_master WHERE type = "table" AND name = '{energy_level}'""")
        exist_status = cursor.fetchall()
        if exist_status == []:# if the selected energy level doesn't exist any table, build a new one
            cursor.execute(f"""create table if not exists '{energy_level}'(name text, cas text, formula text, charge_mass_ratio number, peak_height number, branch_ratio number, optional_fragment text)""")
            cursor.executemany(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?)""", data)
        else:
            molecule = data[0][0]# only one molecule's data could be submitted once!
            status = self.check_exist(energy_level, molecule)
            if status == 0:# if the molecule's data didn't exist in this energy level
                cursor.execute(f"""create table if not exists '{energy_level}'(name text, cas text, formula text, charge_mass_ratio number, peak_height number, branch_ratio number, optional_fragment text)""")
                cursor.executemany(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?)""", data)
            elif status == 1:# if the molecule's data exists
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
                    if mass_exist == 1:# if the molecule's data for this mass exists
                        cursor.execute(f"""UPDATE '{energy_level}' SET peak_height = '{peak_height}' where name = '{molecule}' AND charge_mass_ratio = '{charge_mass_ratio}'""")
                        cursor.execute(f"""UPDATE '{energy_level}' SET branch_ratio = '{branch_ratio}' where name = '{molecule}' AND charge_mass_ratio = '{charge_mass_ratio}'""")
                        cursor.execute(f"""UPDATE '{energy_level}' SET optional_fragment = '{optional_fragment}' where name = '{molecule}' AND charge_mass_ratio = '{charge_mass_ratio}'""")
                    else:
                        cursor.execute(f"""INSERT INTO '{energy_level}' VALUES(?, ?, ?, ?, ?, ?, ?)""", single_row)
        con.commit()
        self.ui.showTable.update()
        con.close()

    def submitToBase(self):
        '''Merge the input data to the original database.'''
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
        cursor_2.execute(f"DROP table if exists '{energy_level}'")# delete the table after being submitted
        self.ui.close()
    
    def check_exist(self, energy_level, molcule):
        '''Check if any molecule's data for specific energy level has already exist'''
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
        self.ui.showTable.update()


    def deleteTable(self):
        energy_level = self.ui.energyOption.currentText()
        energy_level = str(energy_level[2:-3])
        con = sqlite3.connect('temp.db')
        cursor = con.cursor()
        cursor.execute(f"DROP table if exists '{energy_level}'")
        con.close()
        self.ui.showTable.clearContents()

class identity(QtWidgets.QWidget):
    '''This is left for checking identity of users to block users from edit current database directly.'''
    def __init__(self):
        super(identity, self).__init__()
        self.ui = QUiLoader().load('identity.ui')
        self.ui.show()
        self.ui.OkButton.clicked.connect(self.clickOk)
        self.ui.CancelButton.clicked.connect(self.ui.close)
    
    def clickOk(self):
        '''This question could be changed if necessary.'''
        text = self.ui.Input.text()
        if text == 'London':
            self.temp = show_temp()
        else:
            QtWidgets.QMessageBox.about(self.ui,
                'Result',
                'Access denied!')
        self.ui.close()
    
class EditTICS(QtWidgets.QDialog):
    def __init__(self):
        super(EditTICS, self).__init__()
        self.ui = QUiLoader().load('editBEB.ui')
        self.ui.show()
        self.ui.addBEB.clicked.connect(self.add_new_row)
        self.ui.deleteBEB.clicked.connect(self.remove_new_row)
        self.ui.updateBEB.clicked.connect(self.update_data)
        self.ui.submitBEB.setEnabled(False)
        self.ui.submitBEB.clicked.connect(self.submit_data)

    def PrintTICS(self, list):
        list_basic = list[3]
        molecule = list_basic[0]
        con = sqlite3.connect("data-20.db")
        cursor = con.cursor()
        sql = f"SELECT energy, beb FROM 'energy_vs_total_beb' WHERE name = '{molecule}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result != []:
            self.ui.currentBEB.setRowCount(len(result))
            current_row = 0
            for energy in result:
                self.ui.currentBEB.setItem(current_row, 0, QtWidgets.QTableWidgetItem(str(molecule)))
                self.ui.currentBEB.setItem(current_row, 1, QtWidgets.QTableWidgetItem(str(list[3][2])))
                self.ui.currentBEB.setItem(current_row, 2, QtWidgets.QTableWidgetItem(str(energy[0])))
                self.ui.currentBEB.setItem(current_row, 3, QtWidgets.QTableWidgetItem(str(energy[1])))
                current_row = current_row + 1
        else:
            QtWidgets.QMessageBox.information(self.ui,
            'Information',
            "The Total Ionization Cross Section for this molecule is currently empty. Please input data manually.")    
        self.ui.currentBEB.update()

    def add_new_row(self):
        self.ui.currentBEB.insertRow(0)
        self.ui.currentBEB.setItem(0, 0, QtWidgets.QTableWidgetItem(str(self.ui.currentBEB.item(1, 0).text())))
        self.ui.currentBEB.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.ui.currentBEB.item(1, 1).text())))

    def remove_new_row(self):
        currentRow = self.ui.currentBEB.currentRow()
        self.ui.currentBEB.removeRow(currentRow)

    def update_data(self):
        self.ui.currentBEB.update()
        self.ui.submitBEB.setEnabled(True)

    def submit_data(self):
        input_beb = []
        row_num = self.ui.currentBEB.rowCount()
        for i in range(row_num):
            list_input = []
            for j in range(4):
                input = str(self.ui.currentBEB.item(i, j))
                if input == 'None':
                    input = 'N/A'
                else:
                    input = str(self.ui.currentBEB.item(i, j).text())
                list_input.append(input)
            input_beb.append(tuple(list_input))
        choice = QtWidgets.QMessageBox.question(self.ui,
        'Check',
        'Please double check your input before submit the data!')
        if choice == QtWidgets.QMessageBox.No:
            raise ValueError("Pause the program for further check.")
        try: # build connection with the data-20 database 
            con = sqlite3.connect("data-20.db")     
        except sqlite3.Error:
            print(sqlite3.Error)
        cursor = con.cursor()
        for line in input_beb:
            status = self.check_exist(line[2], line[0])
            if status == 1:
                cursor.execute(f"""UPDATE 'energy_vs_total_beb' SET beb = '{line[3]}' where name = '{line[0]}' and energy = '{line[2]}'""")
            else:
                cursor.execute(f"""INSERT INTO 'energy_vs_total_beb'(name, formula, energy, BEB) VALUES(?, ?, ?, ?)""", line)            
        QtWidgets.QMessageBox.about(self.ui,
        'Result',
        'Input Confirmed!')
        con.commit()
        con.close()
        self.ui.close()

    def check_exist(self, energy_level, molcule):
        '''Check if any molecule's TICS for specific energy level has already exist'''
        conn = sqlite3.connect("data-20.db")
        cursor = conn.cursor()
        sql = """select * from 'energy_vs_total_beb'"""
        cursor.execute(sql)
        result = cursor.fetchall()
        status = 0
        for from_db in result:
            if from_db[0] == molcule and str(from_db[2]) == energy_level:
                status = 1
        conn.close()
        return status

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
app = QtWidgets.QApplication([])
PICS = Branching_Ratios()
PICS.ui.show()
app.exec_()