import sqlite3
conn = sqlite3.connect("data-20.db")
cursor = conn.cursor()
# sql = """pragma table_info('main_data')"""
# sql = """select name from sqlite_master where type='table' order by name"""
# sql = """select * from 'energy_vs_total_beb'"""
sql = "SELECT energy, beb FROM 'energy_vs_total_beb' WHERE name = 'Methane'"
# sql="ALTER TABLE 'eighty' RENAME TO 'main_data';"
cursor.execute(sql)
# name = 'qwe'
# cursor.execute(f"""SELECT name from sqlite_master WHERE type = "table" AND name = '{name}'""")
result = cursor.fetchall()
# list1 = []
# status = 0
# for molecule in result:
    # ratio = molecule[5]
    # length = len(str(ratio))
    # if ratio == 0:
    #     list1.append(molecule)
    # if molecule[0] == 'Hexathiane':
    #     list1.append(molecule)
    #     status = 1
# min = min(list1)
# print(min)
# print(list1)
# answer = ''
# for row in result:
#     if row[0] == 'Methane' and row[2] == 70:
#         answer = row[3]
# print(answer)
# # print(type(result))
print(result)
# cursor.execute("DROP table if exists '80 eV'")
conn.close()


# def chart(dict):
#     for a in dict:
#         print(f'''{round(float(a), 5)}: \t{dict[a]}''')

# dict = {'0.016864154795189278': ['¹²C'], '0.04744153020015089': ['¹²C¹H'], '0.09062264234678027': ['¹²C¹H2'], '0.39404429059601476': ['¹²C¹H3'], '0.4437491678870989': ['¹²C¹H4'], '0.007278214174765899': ['¹³C¹H4', '¹²C²H¹H3']}
# chart(dict)

# dict = {'asd': 123, 'qwe': 456, 'zxc': 789}
# print(len(dict))