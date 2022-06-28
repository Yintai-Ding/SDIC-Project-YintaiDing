from load_atom import load_atom
from load_molecule import load_molecule

def check_bond(molecule):
    bonded = []
    molecule_xyz = load_molecule(molecule)
    for i in range(len(molecule_xyz)):
        atom_name_i = molecule_xyz[i]['atom']
        atom_position_i = molecule_xyz[i]['position']
        for j in range(i + 1, len(molecule_xyz)):
            atom_name_j = molecule_xyz[j]['atom']
            atom_position_j = molecule_xyz[j]['position']
            distance = ((float(atom_position_i['x']) - float(atom_position_j['x']))** 2 + (float(atom_position_i['y']) - float(atom_position_j['y'])) ** 2 + (float(atom_position_i['z']) - float(atom_position_j['z'])) ** 2) ** (1./2)
            radius_i = load_atom(atom_name_i)
            radius_j = load_atom(atom_name_j)
            if distance <= (radius_i + radius_j) * 1.2:
                status = 1
                bond_status = {'first atom': atom_name_i + ' ' + str(i), 'second atom': atom_name_j + ' ' + str(j), 'status': status}
                bonded.append(bond_status)
            else:
                status = 0
                bond_status = {'first atom': str(i) + ' ' + atom_name_i, 'second atom': str(j) + ' ' + atom_name_j, 'status': status}
                # bonded.append(bond_status)
    return bonded


if __name__ == '__main__':
    check= check_bond('c6h6')
    for f in check:
        print(f)
    # print(check)