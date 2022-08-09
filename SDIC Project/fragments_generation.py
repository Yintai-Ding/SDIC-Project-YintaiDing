import elements.elements
import os
import itertools
import re

class Generation:
    def __init__(self, molecule):
        self.molecule = molecule

    def load_molecule(self):
        '''load the coordiante of atoms in the molecule and return a dictionary'''
        molecule_xyz = []
        filepath = os.getcwd()
        file_path = os.path.join(filepath, 'geometries', self.molecule + '.xyz')
        try:
            with open(file_path, 'r') as f:
                for i in range(0, 2):
                    next(f)
                content = f.read()
                contact = content.split('\n')
                for line in contact:
                    if line == '' or line.isdigit():
                        continue
                    else:
                        atom = line.split()
                        xyzitem = {'atom': atom[0], 'position': {"x": atom[1], "y": atom[2], "z": atom[3]}}
                        molecule_xyz.append(xyzitem) #store the atoms and relative position into dictionaries and append to a list
            return molecule_xyz
        except:
            return molecule_xyz

    def check_bond(self):
        '''check whether two atoms within a molecule are bonded, this will help the genetation of fragments'''
        bonded = []
        molecule_xyz = self.load_molecule()
        if molecule_xyz != []:
            for i in range(len(molecule_xyz)):
                atom_name_i = molecule_xyz[i]['atom']
                atom_position_i = molecule_xyz[i]['position']
                for j in range(i + 1, len(molecule_xyz)):
                    atom_name_j = molecule_xyz[j]['atom']
                    atom_position_j = molecule_xyz[j]['position']
                    distance = ((float(atom_position_i['x']) - float(atom_position_j['x']))** 2 + (float(atom_position_i['y']) - float(atom_position_j['y'])) ** 2 + (float(atom_position_i['z']) - float(atom_position_j['z'])) ** 2) ** (1./2)
                    radius_i = Atom(atom_name_i).radius
                    radius_j = Atom(atom_name_j).radius
                    if distance <= (radius_i + radius_j) * 1.2: #check the relative position of atoms to check if any bond exist
                        status = 1
                        bond_status = {'first atom': atom_name_i + ' ' + str(i), 'second atom': atom_name_j + ' ' + str(j), 'status': status}
                        bonded.append(bond_status)
                    else:
                        status = 0
                        bond_status = {'first atom': str(i) + ' ' + atom_name_i, 'second atom': str(j) + ' ' + atom_name_j, 'status': status}
        return bonded

    def fragments(self):
        '''this function will return a list with possible fragments and a dictionary which rearrange the fragments
        according to the mass of them'''
        fragments_list = []# a list which contains all fragments and same atom with different positions makes differences
        combine_list = []# all possible combinations from all atoms in molecule
        bonded_list = self.check_bond()# load the list contains all bonds in molecule
        true_fragments_list = []# the list which contains all possible fragments without repeatation
        
        if bonded_list != []:
            for i in range(len(bonded_list)):
                atom_name_1 = bonded_list[i]['first atom']
                atom_name_2 = bonded_list[i]['second atom']
                fragments_list.append(atom_name_1)
                fragments_list.append(atom_name_2)
            fragments_list = list(set(fragments_list))# put single atoms into the list

            for i in range(2, len(fragments_list) + 1):# combinations for two or more atoms
                list_i = list(itertools.combinations((fragments_list), i))
                combine_list.extend(list_i)
            possible_list = []# possible bonded combinations for two or more atoms
            
            fragments_list = [''.join(re.findall(r'[A-Za-z]', x)) for x in fragments_list]
            atom_list = []# list for atoms following the order of alphabet
            for i in fragments_list:
                atom_list.append(i)
            atom_list = sorted(list(set(atom_list)))

            for combination in combine_list:
                list_bonded, tuple_extra = self.generate_combination(combination, bonded_list)
                pieces = ''.join(list_bonded)
                del list_bonded
                possible_list.append(pieces)
                while tuple_extra != ():# check if any missing atoms which are bonded together
                    list_bonded_1, tuple_extra = self.generate_combination(tuple_extra, bonded_list)
                    pieces_1 = ''.join(list_bonded_1)
                    possible_list.append(pieces_1)
                    del list_bonded_1

            fragments_list.extend(possible_list)
            fragments_list = [x for x in fragments_list if x != '']
            fragments_list = list(set(fragments_list))
            dict_by_mass = {}# dictionary which contains the mass of fragments
            for fragment in fragments_list:
                fragment_name = ''
                fragment_mass = 0.0
                single_letter = ''
                for atoms in atom_list:
                    if ''.join(atom_list).count(atoms) >= 2:# this codes is to distinguish some atoms which has repeated letters such as 'C' and 'Cl'
                        single_letter = atoms# the special atom with single letter
                for atoms in atom_list:
                    if atoms.count(single_letter) == 1 and len(atoms) > 1:# the special atom with two letters
                        atom_number = fragment.count(atoms)# number of atom with two letters
                        single_number = fragment.count(single_letter)
                        true_single_number = single_number - atom_number# number of atom with single letter
                        single_position = fragment_name.find(single_letter)
                        if true_single_number == 0:
                            fragment_name = fragment_name[0 : single_position - 2]
                        elif true_single_number == 1:# when the atom number is one, the formula will ignore the number and just leave the atom
                            fragment_name = fragment_name[0 : single_position + 1]
                        else:
                            fragment_name = fragment_name[0 : single_position + 1] + str(true_single_number)
                        if atom_number == 0:
                            continue
                        elif atom_number == 1:
                            fragment_name = fragment_name + self.to_sup(str(round(Atom(atoms).mass))) + atoms
                        else :
                            fragment_name = fragment_name + self.to_sup(str(round(Atom(atoms).mass))) + atoms + str(atom_number)
                        atom_mass = Atom(atoms).mass
                        single_mass = Atom(single_letter).mass
                        fragment_mass = round(fragment_mass + atom_mass * atom_number - single_mass * atom_number)
                    else:# normal molecules steps 
                        atom_number = fragment.count(atoms)
                        if atom_number == 0:
                            continue
                        elif atom_number == 1:
                            fragment_name = fragment_name + self.to_sup(str(round(Atom(atoms).mass))) + atoms
                        elif atom_number > 1:
                            fragment_name = fragment_name + self.to_sup(str(round(Atom(atoms).mass))) + atoms + str(atom_number)
                        atom_mass = Atom(atoms).mass
                        fragment_mass = round(fragment_mass + atom_mass * atom_number)
                true_fragments_list.append(fragment_name)
                if str(fragment_mass) not in dict_by_mass:
                    dict_by_mass[str(fragment_mass)] = [fragment_name]
                else:
                    dict_by_mass[str(fragment_mass)].append(fragment_name)
                    dict_by_mass[str(fragment_mass)] = list(set(dict_by_mass[str(fragment_mass)]))
                    
            true_fragments_list = list(set(true_fragments_list))
        return true_fragments_list

    def generate_combination(self, combination, bonded_list):
        '''The purpose of this function is check the list roughly. The filtration could be done by repeating this function'''
        list_bonded = []# atoms which exist bond connection and could be connected into one fragment
        tuple_extra = ()# exist bond connection but belongs to another fragment
        list_hold = []# possible to join the first list but not tested yet
        any_two = list(itertools.combinations((combination), 2))# for any two atoms in the combination
        
        for two_atom in any_two:
            for i in range(len(bonded_list)):
                if two_atom[0] == bonded_list[i]['first atom'] or two_atom[0] == bonded_list[i]['second atom']:
                    if two_atom[1] == bonded_list[i]['first atom'] or two_atom[1] == bonded_list[i]['second atom']:
                        if list_bonded == []:# if the list is currently empty, add two atoms to list
                            list_bonded.append(two_atom[0])
                            list_bonded.append(two_atom[1])
                        elif two_atom[0] in list_bonded and two_atom[1] not in list_bonded:# if any atom exists in the list, then they could connect together as a fragment
                            list_bonded.append(two_atom[1])
                        elif two_atom[0] not in list_bonded and two_atom[1] in list_bonded:
                            list_bonded.append(two_atom[0])
                        elif two_atom[0] in list_bonded and two_atom[1] in list_bonded:
                            list_bonded.append('')# repeated atoms in list
                        else:
                            list_hold.append(two_atom)
        # since the code above is checking through the list, there may be atoms that could be connected together but appears in the list to early before could be found in the list
        if list_hold != []: #repeat the step above to avoid missing atoms that could be connected
            list_hold_old = []
            while list_hold != list_hold_old: #check if any two atom group has been connected to fragment
                tuple_extra = () # initialize the tuple of atoms belongs to other fragments
                list_hold_old = list_hold #if the list doesn't change after the loop, there is no group of atoms to be connected to the fragment
                for two_atom_hold in list_hold:
                    if two_atom_hold[0] in list_bonded and two_atom_hold[1] not in list_bonded:
                        list_bonded.append(two_atom_hold[1])
                        list_hold.remove(two_atom_hold)
                    elif two_atom_hold[0] not in list_bonded and two_atom_hold[1] in list_bonded:
                        list_bonded.append(two_atom_hold[0])
                        list_hold.remove(two_atom_hold)
                    elif two_atom_hold[0] in list_bonded and two_atom_hold[1] in list_bonded:
                        list_bonded.append('')
                        list_hold.remove(two_atom_hold)
                    else:
                        tuple_atom = (two_atom_hold[0], two_atom_hold[1])
                        tuple_extra = tuple_extra + tuple_atom
        list_bonded = list(set(list_bonded))
        tuple_extra = tuple(set(tuple_extra))# not connected to this fragment but belongs to other fragments
        return list_bonded, tuple_extra
    
    def to_sup(self, strings):
        '''Add superscript to formula for further comparison'''
        sups = {u'0': u'\u2070',
                u'1': u'\xb9',
                u'2': u'\xb2',
                u'3': u'\xb3',
                u'4': u'\u2074',
                u'5': u'\u2075',
                u'6': u'\u2076',
                u'7': u'\u2077',
                u'8': u'\u2078',
                u'9': u'\u2079'}
        return ''.join(sups.get(char, char) for char in strings)

class Atom:
    def __init__(self, atom):
        self.symbol = atom #this class will generate atoms with properties radius and mass
        self.radius = elements.elements.RADIUS[atom]
        self.mass = elements.elements.MASS[atom]