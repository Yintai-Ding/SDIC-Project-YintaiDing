import sqlite3

def connection(molecule):
    conn = sqlite3.connect("data-20.db")
    cursor = conn.cursor()
    sql = """select * from name"""
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
    conn.close()
    return(dict_fragments, dict_mass, total_ratio)

def translate_cas(casCode):
    conn = sqlite3.connect("data-20.db")
    cursor = conn.cursor()
    sql = """select * from name"""
    cursor.execute(sql)
    result = cursor.fetchall()
    for case in result:
        if case[1] == casCode:
            molecule = str(case[0])
    conn.close()
    return(molecule)

def translate_formula(formula):
    conn = sqlite3.connect("data-20.db")
    cursor =conn.cursor()
    sql = """select * from name"""
    cursor.execute(sql)
    result = cursor.fetchall()
    for case in result:
        if case[3] == formula:
            molecule = str(case[0])
    conn.close()
    return(molecule)