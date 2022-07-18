import sqlite3

def connection(molecule):
    molecule_exist = 0
    conn = sqlite3.connect("data-20.db")
    cursor = conn.cursor()
    sql = """select * from eighty"""
    cursor.execute(sql)
    result = cursor.fetchall()
    dict_fragments = {}
    dict_mass = {}
    total_ratio = 0
    for case in result:
        if case[0] == molecule:
            dict_fragments[str(case[6])] = case[7].split(',')
            dict_mass[str(case[6])] = case[4]
            total_ratio = total_ratio + case[6]
            molecule_exist = 1
    conn.close()
    if molecule_exist == 0:
        raise ValueError("The input molecule name doesn't exist in current data base.")
    return(dict_fragments, dict_mass, total_ratio)

def translate_cas(casCode):
    cas_exist = 0
    conn = sqlite3.connect("data-20.db")
    cursor = conn.cursor()
    sql = """select * from eighty"""
    cursor.execute(sql)
    result = cursor.fetchall()
    for case in result:
        if case[1] == casCode:
            molecule = str(case[0])
            cas_exist = 1
    conn.close()
    if cas_exist == 0:
        raise ValueError("The input cas number doesn't exist in current data base.")
    return(molecule)

def translate_formula(formula):
    formula_exist = 0
    list_formula = []
    conn = sqlite3.connect("data-20.db")
    cursor =conn.cursor()
    sql = """select * from eighty"""
    cursor.execute(sql)
    result = cursor.fetchall()
    for case in result:
        if case[3] == formula:
            molecule = str(case[0])
            list_formula.append(molecule)
            formula_exist = 1
    conn.close()
    if formula_exist == 0:
        raise ValueError("The input formula doesn't exist in current data base.")
    if len(set(list_formula)) > 1:
        raise ValueError("Your input formula exists isomers. Please try more accurate input.")
    return(molecule)