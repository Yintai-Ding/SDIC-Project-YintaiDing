import sqlite3
from fragments_generation import * 

def check(formula, name):
    '''Load fragments of molecule from database and generated from functions. Make comparison and check missing fragments'''
    molecule_YT = Generation(formula)# use the formula to generate possible fragments through bonds
    list_YT, dict_YT = molecule_YT.fragments()
    conn = sqlite3.connect("data-20.db")# use the name of molecule to load possible fragments from database
    cursor = conn.cursor()
    sql = """select * from 'main_data'"""
    cursor.execute(sql)
    result = cursor.fetchall()
    list_LF = []
    for molecule in result:
        if molecule[0] == name:
            list_LF.extend(molecule[6].split(','))
    intersection = set(list_LF).intersection(set(list_YT))# fragments that exist in both list
    difference_YT = set(list_YT).difference(set(list_LF))# fragments that might missed from the database
    difference_LF = set(list_LF).difference(set(list_YT))# fragments that include isotope atoms 
    print(f'The intersection of two methods: {intersection}')
    print(f'Unexpected fragments in database: {difference_LF}')
    print(f'Possible missing fragments in database: {difference_YT}')
    conn.close()

check('ccl4', 'Carbon Tetrachloride')