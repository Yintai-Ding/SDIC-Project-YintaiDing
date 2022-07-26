import sqlite3
from fragments_generation import * 

def check(formula, name):
    # molecule_YT = Generation('ccl4')
    molecule_YT = Generation(formula)
    list_YT, dict_YT = molecule_YT.fragments()
    conn = sqlite3.connect("data-20.db")
    cursor = conn.cursor()
    sql = """select * from '70 eV'"""
    cursor.execute(sql)
    result = cursor.fetchall()
    list_LF = []
    for molecule in result:
        # if molecule[0] == 'Carbon Tetrachloride':
        if molecule[0] == name:
            list_LF.extend(molecule[6].split(','))
    intersection = set(list_LF).intersection(set(list_YT))
    difference_YT = set(list_YT).difference(set(list_LF))
    difference_LF = set(list_LF).difference(set(list_YT))
    print(f'The intersection of two methods: {intersection}')
    print(f'Unexpected fragments in database: {difference_LF}')
    print(f'Possible missing fragments in database: {difference_YT}')
    conn.close()

check('ccl4', 'Carbon Tetrachloride')