import sqlite3

def connection(molecule):
    '''Link to database of 70 eV and load data as dictionaries and lists'''
    molecule_exist = 0
    conn = sqlite3.connect("data-20.db")
    cursor = conn.cursor()
    sql = """select * from 'main_data'"""
    cursor.execute(sql)
    result = cursor.fetchall()
    dict_fragments = {}
    dict_mass = {}
    dict_peak = {}
    molecule_cas, molecule_formula = '', ''
    total_ratio = 0
    for case in result:
        if case[0] == molecule:
            dict_fragments[str(case[5])] = case[6]
            dict_mass[str(case[5])] = case[3]
            dict_peak[str(case[5])] = case[4]
            total_ratio = total_ratio + case[5]
            molecule_exist = 1
            molecule_cas = case[1]
            molecule_formula = case[2]
    conn.close()
    list_basic = [molecule, molecule_cas, molecule_formula]
    return(dict_fragments, dict_mass, dict_peak, total_ratio, molecule_exist, list_basic)

def translate_cas(casCode):
    '''Transform the CAS number input to name of molecule'''
    molecule = ''
    cas_exist = 0
    conn = sqlite3.connect("data-20.db")
    cursor = conn.cursor()
    sql = """select * from 'main_data'"""
    cursor.execute(sql)
    result = cursor.fetchall()
    for case in result:
        if case[1] == casCode:
            molecule = str(case[0])
            cas_exist = 1
    conn.close()
    return(molecule, cas_exist)

def translate_formula(formula):
    '''Transform the formula of molecule to name'''
    molecule = ''
    formula_exist = 0
    list_formula = []
    conn = sqlite3.connect("data-20.db")
    cursor =conn.cursor()
    sql = """select * from 'main_data'"""
    cursor.execute(sql)
    result = cursor.fetchall()
    for case in result:
        if case[2] == formula:
            molecule = str(case[0])
            list_formula.append(molecule)
            formula_exist = 1
    conn.close()
    return(molecule, formula_exist, list_formula)