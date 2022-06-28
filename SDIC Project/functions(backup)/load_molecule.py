import os
def load_molecule(molecule):
    molecule_xyz = []
    filepath = os.getcwd()
    file_path = filepath + '\\geometries\\' + molecule + '.xyz'
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
                molecule_xyz.append(xyzitem)
    return molecule_xyz

if __name__ == '__main__':
    xyz = load_molecule('ch4')
    for f in xyz:
        print(f)