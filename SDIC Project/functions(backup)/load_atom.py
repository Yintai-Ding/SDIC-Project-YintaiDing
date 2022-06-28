import elements.elements
def load_atom(atom):
   atom_radius = elements.elements.RADIUS[atom]
   return atom_radius

if __name__ == '__main__':
    xyz = load_atom('c'.upper())
    print(xyz)