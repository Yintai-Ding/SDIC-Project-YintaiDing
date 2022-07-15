import sqlite3
from fragments_generation import * 

molecule_YT = Generation('ccl4')
list_YT, dict_YT = molecule_YT.fragments()
conn = sqlite3.connect("data-20.db")
cursor = conn.cursor()
sql = """select * from eighty"""
cursor.execute(sql)
result = cursor.fetchall()
list_LF = []
for molecule in result:
    if molecule[0] == 'Carbon Tetrachloride':
        list_LF.extend(molecule[7].split(','))
intersection = set(list_LF).intersection(set(list_YT))
difference_YT = set(list_YT).difference(set(list_LF))
difference_LF = set(list_LF).difference(set(list_YT))
print(f'The intersection of two methods: {intersection}')
print(f'Unexpected fragments in database: {difference_LF}')
print(f'Possible missing fragments in database: {difference_YT}')
conn.close()
