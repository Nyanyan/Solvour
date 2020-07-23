'''
Solver:
* "X" twist includes X, X2, X', while "X2" means only X2
--- Reduction phase ---
phase 0: gather RL centers on RL faces
         use R, Rw, L, U, Uw, D, F, Fw, B
phase 1: gather FB centers on FB faces, separate low & high edges, clear RL center parity, avoid last two edges
         use R, Rw, L, U, Uw2, D, F, Fw2, B
phase 2: make center columns and pair up 4 edges on the middle layer
         use R2, Rw2, L2, U, Uw2, D, F, Fw2, B
phase 3: complete center, edge pairing and clear edge parity (= PP), which means complete reduction
         use R2, Rw2, L2, U, Uw2, D, F2, Fw2, B2
--- 3x3x3 phase ---
phase 4: gather UD stickers on UD faces and clear EO
         use R, L, U, D, F, B, not use R2, L2, F2, B2
phase 5: solve it!
         use R2, L2, U, D, F2, B2
'''


from cube_class import Cube, face, axis, wide
from time import time

def move_ep_phase1_func(puzzle_arr, twist):
    decision = [
        [[], [], [2, 3, 6, 7], [18, 19, 22, 23], [11, 10, 9, 8], [15, 14, 13, 12]], 
        [[12, 13, 10, 11], [8, 9, 14, 15], [0, 1, 4, 5], [16, 17, 20, 21], [], []],
        [[3, 2, 19, 18], [7, 6, 23, 22], [], [], [5, 4, 17, 16], [1, 0, 21, 20]]
        ]
    mse_lst = [[0, 0], [0, 1], [1, 2], [1, 3], [0, 2], [0, 3], [1, 0], [1, 1], [2, 1], [2, 0], [2, 3], [2, 2], [2, 5], [2, 4], [2, 7], [2, 6], [0, 4], [0, 5], [1, 4], [1, 5], [0, 6], [0, 7], [1, 6], [1, 7]]
    res = [-1, -1, -1]
    puzzle = [puzzle_arr // 65536, (puzzle_arr // 256) % 256, puzzle_arr % 256]
    for mse in range(3):
        decision_num = 0
        #print('decision', decision[mse][twist // 6])
        for i in decision[mse][twist // 6]:
            m_mse = mse_lst[i][0]
            shift = mse_lst[i][1]
            #print('shift', shift)
            decision_num *= 2
            #print(int((puzzle[m_mse] >> (7 - shift)) & 1 != i % 2))
            decision_num += int((puzzle[m_mse] >> (7 - shift)) & 1)
        #print('dec', decision_num)
        #print(move_ep_phase1[mse][puzzle[mse]][twist_to_idx[twist]])
        res[mse] = move_ep_phase1[mse][puzzle[mse]][twist_to_idx[twist]][decision_num]
    res = res[0] * 65536 + res[1] * 256 + res[2]
    return res

def initialize_puzzle_arr(phase, puzzle):
    if phase == 0:
        return [puzzle.idx_ce_phase0()]
    elif phase == 1:
        return [puzzle.idx_ce_phase1_fbud() * 70 + puzzle.idx_ce_phase1_rl(), puzzle.idx_high_low_edge()]

def distance(puzzle_arr, phase):
    puzzle = puzzle_arr if phase != 1 else [puzzle_arr[0], puzzle_arr[1] // 2]
    return max(prunning[phase][i][puzzle[i]] for i in range(prun_len[phase]))

def move_arr(puzzle_arr, phase, twist):
    if phase == 0:
        return [move_ce_phase0[puzzle_arr[0]][twist_to_idx[twist]]]
    elif phase == 1:
        return [move_ce_phase1_fbud[puzzle_arr[0] // 70][twist_to_idx[twist]] * 70 + move_ce_phase1_rl[puzzle_arr[0] % 70][twist_to_idx[twist]], move_ep_phase1_func(puzzle_arr[1], twist)]

def phase_search(phase, puzzle_arr, depth):
    global path
    if depth == 0:
        if distance(puzzle_arr, phase) == 0:
            return True
    else:
        if distance(puzzle_arr, phase) <= depth:
            l1_twist = path[-1] if len(path) >= 1 else -10
            l2_twist = path[-2] if len(path) >= 2 else -10
            l3_twist = path[-3] if len(path) >= 3 else -10
            for twist in successor[phase]:
                if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
                    continue
                n_puzzle_arr = move_arr(puzzle_arr, phase, twist)
                path.append(twist)
                if phase_search(phase, n_puzzle_arr, depth - 1):
                    return True
                path.pop()

def solver(puzzle):
    global solution, path
    solution = []
    for phase in range(2):
        print('phase', phase, 'depth', end=' ',flush=True)
        strt = time()
        for depth in range(15):
            print(depth, end=' ', flush=True)
            path = []
            puzzle_arr = initialize_puzzle_arr(phase, puzzle)
            if phase_search(phase, puzzle_arr, depth):
                for twist in path:
                    puzzle = puzzle.move(twist)
                solution.extend(path)
                #print('phase', phase, end=': ')
                print('')
                for i in path:
                    print(move_candidate[i], end=' ')
                print('')
                print(time() - strt, 'sec')
                break

#                  0    1     2     3     4      5      6    7     8     9     10     11     12   13    14    15    16     17     18   19   20     21    22     23     24   25    26    27    28     29     30   31    32    33    34     35
move_candidate = ["R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "Lw", "Lw2", "Lw'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "Dw", "Dw2", "Dw'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'", "Bw", "Bw2", "Bw'"]
twist_to_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, -1, -1, -1, 9, 10, 11, 12, 13, 14, 15, 16, 17, -1, -1, -1, 18, 19, 20, 21, 22, 23, 24, 25, 26, -1, -1, -1]

successor = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14, 15, 16, 17, 18, 19, 20,             24, 25, 26, 27, 28, 29, 30, 31, 32            ], # phase 0
            [0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            ], # phase 1
            [   1,       4,       7,               12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            ], # phase 2
            [   1,       4,       7,               12, 13, 14,             18, 19, 20,                 25,         28,         31,               ], # phase 3
            [0,    2,          6,    8,            12, 13, 14,             18, 19, 20,             24,     26,             30,     32            ], # phase 4
            [   1,                7,               12, 13, 14,             18, 19, 20,                 25,                     31                ]  # phase 5
            ]

move_ce_phase0 = [[] for _ in range(735471)]
with open('move_table/move_ce_phase0.csv', mode='r') as f:
    for idx in range(735471):
        move_ce_phase0[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ce_phase1_fbud = [[] for _ in range(12870)]
with open('move_table/move_ce_phase1_fbud.csv', mode='r') as f:
    for idx in range(12870):
        move_ce_phase1_fbud[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ce_phase1_rl = [[] for _ in range(70)]
with open('move_table/move_ce_phase1_rl.csv', mode='r') as f:
    for idx in range(70):
        move_ce_phase1_rl[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ep_phase1 = [[[[] for _ in range(27)] for _ in range(256)] for _ in range(3)]
with open('move_table/move_ep_phase1.csv', mode='r') as f:
    for mse in range(3):
        for all_twist in range(256):
            for twist in range(27):
                move_ep_phase1[mse][all_twist][twist] = [int(i) for i in f.readline().replace('\n', '').split(',')]


prunning = [None for _ in range(6)]
prun_len = [1, 2, 3, 3, 2, 3]
for phase in range(2):
    prunning[phase] = [[] for _ in range(prun_len[phase])]
    with open('prun_table/prunning' + str(phase) + '.csv', mode='r') as f:
        for lin in range(prun_len[phase]):
            prunning[phase][lin] = [int(i) for i in f.readline().replace('\n', '').split(',')]

solution = []
path = []
scramble = [move_candidate.index(i) for i in input("scramble: ").split()]
puzzle = Cube()
for mov in scramble:
    puzzle = puzzle.move(mov)
strt = time()
solver(puzzle)
print('solution:',end=' ')
#print(solution)
for i in solution:
    print(move_candidate[i],end=' ')
print('')
print(len(solution), 'moves')
print(time() - strt, 'sec')





