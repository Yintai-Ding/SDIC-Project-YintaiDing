import numpy as np
from fragments_generation import *


dict = np.load('processed_data.npy', allow_pickle = True).item()
formula = dict['Methane']['formula'].replace(" ", "")
fragments = dict['Methane']['optional_fragments']
test = Generation(formula.lower())
list, dict = test.fragments()
# print(dict.values())
# print(fragments)
list_LF = []
for fragment in fragments:
    for things in fragment:
        list_LF.append(things)
list_YT = []
for fragment in dict.values():
    for things in fragment:
        list_YT.append(things)
intersection = set(list_LF).intersection(set(list_YT))
difference = set(list_LF).symmetric_difference(set(list_YT))
difference_YT = set(list_YT).difference(set(list_LF))
difference_LF = set(list_LF).difference(set(list_YT))
# number_match = 0
# for fragment_1 in dict.values():
#     for fragment_2 in fragments:
#         if fragment_1 == fragment_2:
#             number_match = number_match + 1
# print(number_match)
print(intersection)
print(difference)
print(f'Missing fragments: ', difference_YT)
print(f'Unexpected fragments: ', difference_LF)