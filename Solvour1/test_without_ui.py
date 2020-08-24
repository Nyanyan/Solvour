import subprocess

# scramble: L2 B L2 F' R2 F' D2 B D2 L D2 B2 D2 F2 D F R U L' Fw2 R U2 Rw2 F L2 F2 Rw2 B' R B' Rw2 Uw' R' U' Rw2 F' R' Fw' Uw' Fw' Rw2 B2 Rw U'
state = [
    0, 2, 2, 5, 2, 2, 3, 3, 4, 5, 1, 0, 1, 1, 5, 0, # D
    0, 2, 4, 2, 2, 1, 0, 5, 5, 2, 5, 5, 1, 0, 2, 4, # B
    2, 1, 3, 3, 1, 4, 0, 0, 0, 5, 4, 5, 1, 0, 0, 4, # U
    5, 2, 2, 1, 3, 0, 4, 1, 4, 1, 0, 4, 3, 5, 1, 2, # F
    0, 4, 4, 5, 5, 1, 2, 3, 1, 4, 3, 3, 3, 4, 3, 3, # R
    5, 0, 3, 4, 1, 3, 3, 4, 3, 2, 5, 0, 2, 1, 5, 4  # L
    ]

'''
state = [ # DP state
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 
    0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
    4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
    4, 4, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4
    ]
'''
'''
state = [ # OP state
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 
    1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4
    ]
'''

#                   0    1     2     3     4      5      6    7     8     9     10     11     12   13    14    15    16     17     18   19   20     21    22     23     24   25    26    27    28     29     30   31    32    33    34     35
move_candidate = ["R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "Lw", "Lw2", "Lw'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "Dw", "Dw2", "Dw'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'", "Bw", "Bw2", "Bw'"]
#solution = solver(state, [0.5, 5, 2, 2, 2, 3], 30)
# R U Fw L2 F2 B Uw2 Rw' R F'
# reverse: F R' Rw Uw2 B' F2 L2 Fw' U' R'
#solution = [0, 12, 27, 7, 25, 30, 16, 5, 0, 26]
# Rw2 Fw D' Fw L' R Uw L2 F2 Rw
# reverse Rw' F2 L2 Uw' R' L Fw' D Fw' Rw2
#solution = [4, 27, 20, 27, 8, 0, 15, 7, 25, 3]
# Rw2 Fw D' Fw B' R Uw L2 F2 Rw R U Fw L2 F2 B Uw2 Rw' R F'
# rev F R' Rw Uw2 B' F2 L2 Fw' U' R' Rw' F2 L2 Uw' R' B Fw' D Fw' Rw2
#solution = [4, 27, 20, 27, 32, 0, 15, 7, 25, 3, 0, 12, 27, 7, 25, 30, 16, 5, 0, 26]
# Fw B' R Uw L2 F2 Rw R U Fw
# rev Fw' U' R' Rw' F2 L2 Uw' R' B Fw'
state_reshape = [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16]
face_coord = ['U', 'F', 'R', 'B', 'L', 'D']
state_str = ''.join([face_coord[state[i]] for i in state_reshape])
solution_str = subprocess.check_output(['java', '-cp', '.:threephase.jar:twophase.jar', 'solver', state_str])
print(solution_str)
solution = ''
for i in solution_str.split():
    if not i in move_candidate:
        break
    else:
        solution.append(move_candidate.index(i))
print(solution)