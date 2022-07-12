import sqlite3
from fragments_generation import * 

molecule_YT = Generation('ch4')
list_YT, dict_YT = molecule_YT.fragments()
conn = sqlite3.connect("test.db")
cursor = conn.cursor()
sql = """select * from name"""
cursor.execute(sql)
result = cursor.fetchall()
list_LF = []
for molecule in result:
    if molecule[0] == 'Methane':
        list_LF.extend(molecule[3].split(','))
intersection = set(list_LF).intersection(set(list_YT))
difference_YT = set(list_YT).difference(set(list_LF))
difference_LF = set(list_LF).difference(set(list_YT))
print(intersection)
print(difference_LF)
print(difference_YT)
conn.close()
