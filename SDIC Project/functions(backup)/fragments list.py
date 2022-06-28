from bonded import check_bond
import itertools
import re

def fragments(molecule):
    fragments_list = []#盛放最终可能fragments的列表
    combine_list = []#以原子组合为起点，从所有的原子中选取可能的组合
    bonded_list = check_bond(molecule)
    true_fragments_list = []
    
    for i in range(len(bonded_list)):
        atom_name_1 = bonded_list[i]['first atom']
        atom_name_2 = bonded_list[i]['second atom']
        fragments_list.append(atom_name_1)
        fragments_list.append(atom_name_2)
    fragments_list = list(set(fragments_list))#单个原子进入组合
    # for i in range(len(bonded_list)):#根据键的断裂两端来生成碎片，但不知道两端的bonded要判断到什么程度，且多键断裂情况不好计算
    #     fragment_1, fragment_2 = []
    #     part_1 = bonded_list[i]['first atom']
    #     part_2 = bonded_list[i]['second atom']
    #     for j in range(len(bonded_list)):
    #         if i != j and bonded_list[j]['first atom'] == part_1 or bonded_list[j]['second atom'] == part_1:
    for i in range(2, len(fragments_list) + 1):#根据总体的原子组合进行碎片生成,从两个一组最后到全部
        list_i = list(itertools.combinations((fragments_list), i))
        combine_list.extend(list_i)
    possible_list = []#两个以上的组合可能性
    
    for combination in combine_list:
        list_not_bonded, tuple_extra = generate_combination(combination, bonded_list)
        pieces = ''.join(list_not_bonded)
        del list_not_bonded
        possible_list.append(pieces)
        while tuple_extra != ():
            list_not_bonded_1, tuple_extra = generate_combination(tuple_extra, bonded_list)
            pieces_1 = ''.join(list_not_bonded_1)
            possible_list.append(pieces_1)
            del list_not_bonded_1

    fragments_list = [''.join(re.findall(r'[A-Za-z]', x)) for x in fragments_list]
    atom_list = []
    for i in fragments_list:
        atom_list.append(i)
    atom_list = list(set(atom_list))
    fragments_list.extend(possible_list)
    fragments_list = [x for x in fragments_list if x != '']
    fragments_list = list(set(fragments_list))
    for fragment in fragments_list:
        fragment_name = ''
        for atom in atom_list:
            atom_number = fragment.count(atom)
            if atom_number == 0:
                continue
            elif atom_number == 1:
                fragment_name = fragment_name + atom
            else :
                fragment_name = fragment_name + atom + str(atom_number)
        true_fragments_list.append(fragment_name)
    true_fragments_list = list(set(true_fragments_list))
    return true_fragments_list

def generate_combination(combination, bonded_list):
    list_not_bonded = []#能够确认存在bonded关系并能连接在一起的原子
    tuple_extra = ()#存在bonded关系但无法跟上一列表中原子连接的原子
    list_hold = []#可能与bonded存在链接关系，但并未遍历认证
    any_two = list(itertools.combinations((combination), 2))
    
    for two_atom in any_two:
        for i in range(len(bonded_list)):
            if two_atom[0] == bonded_list[i]['first atom'] or two_atom[0] == bonded_list[i]['second atom']:
                if two_atom[1] == bonded_list[i]['first atom'] or two_atom[1] == bonded_list[i]['second atom']:
                    if list_not_bonded == []:
                        list_not_bonded.append(two_atom[0])
                        list_not_bonded.append(two_atom[1])
                    elif two_atom[0] in list_not_bonded and two_atom[1] not in list_not_bonded:
                        list_not_bonded.append(two_atom[1])
                    elif two_atom[0] not in list_not_bonded and two_atom[1] in list_not_bonded:
                        list_not_bonded.append(two_atom[0])
                    elif two_atom[0] in list_not_bonded and two_atom[1] in list_not_bonded:
                        list_not_bonded.append('')
                    else:
                        list_hold.append(two_atom)
    if list_hold != []:
        for two_atom_hold in list_hold:
            if two_atom_hold[0] in list_not_bonded and two_atom_hold[1] not in list_not_bonded:
                list_not_bonded.append(two_atom_hold[1])
            elif two_atom_hold[0] not in list_not_bonded and two_atom_hold[1] in list_not_bonded:
                list_not_bonded.append(two_atom_hold[0])
            elif two_atom_hold[0] in list_not_bonded and two_atom_hold[1] in list_not_bonded:
                list_not_bonded.append('')
            else:
                tuple1 = (two_atom[0], two_atom[1])
                tuple_extra = tuple_extra + tuple1
    list_not_bonded = list(set(list_not_bonded))
    tuple_extra = tuple(set(tuple_extra))
    return list_not_bonded, tuple_extra

if __name__ == '__main__':
    list = fragments('c6h6')
    if list == []:
        print('The atoms are not connected!')
    else:
        print(list)
    # for a in list:
    #     if a.count('C 0') >= 2:
    #         print(a)
