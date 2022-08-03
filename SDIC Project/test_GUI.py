import sqlite3
from fragments_generation import *
from read_db import *

def test_generate_fragments():
    '''Load fragments of molecule from database and generated from functions. Make comparison and check missing fragments'''
    molecule_generate = Generation("Methane")# use the name to generate possible fragments through bonds
    list_generate = molecule_generate.fragments()
    conn = sqlite3.connect("data-20.db")# use the name of molecule to load possible fragments from database
    cursor = conn.cursor()
    sql = """select * from 'main_data'"""
    cursor.execute(sql)
    result = cursor.fetchall()
    list_database = []
    for molecule in result:
        if molecule[0] == "Methane":
            list_database.extend(molecule[6].split(','))
    intersection = set(list_database).intersection(set(list_generate))# fragments that exist in both list
    difference_generate = set(list_generate).difference(set(list_database))# fragments that might missed from the database
    difference_database = set(list_database).difference(set(list_generate))# fragments that include isotope atoms 
    conn.close()
    expectation_intersection = {'¹²C¹H3', '¹²C', '¹²C¹H4', '¹²C¹H', '¹²C¹H2'}
    expectation_generate = {'¹H'}
    expectation_database = {'¹³C¹H4', '¹²C²H¹H3'}
    assert intersection == expectation_intersection
    assert difference_generate == expectation_generate
    assert difference_database == expectation_database

def test_load_molecule():
    '''When the molecule's relative position is not available now, the function should return a empty list.'''
    molecule = Generation("not_exist")
    position_list = molecule.load_molecule()
    assert position_list == []

def test_check_bond():
    '''When the imput molecule is not available, the function shold return a empty list and not raise error.'''
    molecule = Generation("not_exist")
    bond_list = molecule.check_bond()
    assert bond_list == []

def test_translate_cas():
    '''Test if the function could translate the cas number to name of molecule correctly.'''
    cas_number = '74-82-8'
    molecule, cas_exist = translate_cas(cas_number)
    assert molecule == 'Methane'
    assert cas_exist == 1

def test_translate_cas_wrong():
    '''When the cas number doesn't exist in database, the function should return the exist status as 0'''
    cas_number = 'wrong_number'
    molecule, cas_exist = translate_cas(cas_number)
    assert molecule == ''
    assert cas_exist == 0

def test_translate_formula():
    '''Test if the function could translate the formula to name of molecule correctly.'''
    formula = 'CH4'
    molecule, formula_exist, list_formula = translate_formula(formula)
    assert molecule == 'Methane'
    assert formula_exist == 1
    assert set(list_formula) == {'Methane'}

def test_translate_formula_wrong():
    '''When the formula doesn't exist in database, the function should return the exist status as 0'''
    formula = 'wrong_formula'
    molecule, formula_exist, list_formula = translate_formula(formula)
    assert molecule == ''
    assert formula_exist == 0
    assert set(list_formula) == set()

def test_translate_formula_isotope():
    '''When the formula exist in isomerss, the function should return a list of iosmers'''
    formula = 'C6H6'
    molecule, formula_exist, list_formula = translate_formula(formula)
    assert formula_exist == 1
    assert set(list_formula) == {'1,5-Hexadiyne', '2,4-Hexadiyne', '1,3-Hexadien-5-yne', '1,5-Hexadien-3-yne', 'Benzene'}

def test_connection_wrong():
    '''When the molecule doesn't exist in database, the function should return the exist status as 0'''
    molecule = 'wrong_molecule'
    dict_fragments, dict_mass, dict_peak, total_ratio, molecule_exist, list_basic = connection(molecule)
    assert molecule_exist == 0