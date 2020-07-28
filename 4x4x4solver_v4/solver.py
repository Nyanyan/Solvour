'''
Solver:
* "X" twist includes X, X2, X', while "X2" means only X2
--- Reduction phase ---
phase 0: gather RL centers on RL faces
         use R, Rw, L, U, Uw, D, F, Fw, B
phase 1: gather FB centers on FB faces, separate low & high edges, clear RL center parity, avoid last two edges (, which means clear OLL Parity)
         use R, Rw, L, U, Uw2, D, F, Fw2, B
phase 2: make center columns and pair up 4 edges on the middle layer
         use R2, Rw2, L2, U, Uw2, D, F, Fw2, B
phase 3: complete center, edge pairing and clear edge parity (= PLL Parity), which means complete reduction
         use R2, Rw2, L2, U, Uw2, D, F2, Fw2, B2
--- 3x3x3 phase ---
phase 4: gather UD stickers on UD faces and clear EO
         use R, L, U, D, F, B, not use R2, L2, F2, B2
phase 5: solve it!
         use R2, L2, U, D, F2, B2
'''


from cube_class import Cube, face, axis, wide, move_cp, move_co, move_ep, move_ce, move_candidate, twist_to_idx, successor, ep_switch_parity, idx_ep_phase1
from time import time
from math import sqrt

def initialize_puzzle_arr(phase, puzzle):
    if phase == 0:
        return [puzzle.idx_ce_phase0()]
    elif phase == 1:
        return [puzzle.idx_ce_phase1_fbud() * 70 + puzzle.idx_ce_phase1_rl(), idx_ep_phase1(puzzle.Ep)]

def move_arr(puzzle_arr, phase, twist):
    if phase == 0:
        return [move_ce_phase0[puzzle_arr[0]][twist_to_idx[twist]]]
    elif phase == 1:
        return [move_ce_phase1_fbud[puzzle_arr[0] // 70][twist_to_idx[twist]] * 70 + move_ce_phase1_rl[puzzle_arr[0] % 70][twist_to_idx[twist]], move_ep_phase1[puzzle_arr[1]][twist_to_idx[twist]]]

def distance(puzzle_arr, phase):
    lst = [prunning[phase][i][puzzle_arr[i]] for i in range(prun_len[phase])]
    mx = max(lst)
    #sm = sqrt(sum([i ** 2 for i in lst]))
    sm = sum(lst)
    shift1 = 2
    ratio1 = pow(2, mx - shift1)
    shift2 = 3
    ratio2 = pow(3, shift2 - sm)
    res = int((sm * ratio1 + mx * ratio2) / (ratio1 + ratio2))
    #print(mx, sm, ratio1, ratio2, res)
    if res == 0 and phase == 1:
        puzzle_ep = [i for i in puzzle.Ep]
        for i in path:
            puzzle_ep = move_ep(puzzle_ep, i)
        if ep_switch_parity(puzzle_ep):
            print('a', end='')
            return 99
    return res

def phase_search(phase, puzzle_arr, depth):
    global path, cnt, blacklist
    dis = distance(puzzle_arr, phase)
    if dis == 99:
        blacklist.add(path[0])
        return 99
    #print(l_dis, dis)
    if depth == 0:
        if dis == 0:
            #print(depth, dis)
            return True
    else:
        if dis <= depth:
            l1_twist = path[-1] if len(path) >= 1 else -10
            l2_twist = path[-2] if len(path) >= 2 else -10
            l3_twist = path[-3] if len(path) >= 3 else -10
            for twist in successor[phase]:
                if (len(path) == 0 and twist in blacklist) or face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
                    continue
                cnt += 1
                n_puzzle_arr = move_arr(puzzle_arr, phase, twist)
                path.append(twist)
                tmp = phase_search(phase, n_puzzle_arr, depth - 1)
                if tmp == 99:
                    path.pop()
                    if len(path) == 0:
                        continue
                    else:
                        return 99
                if tmp:
                    #print(depth, dis)
                    return True
                path.pop()
    return False

def solver():
    global solution, path, cnt, puzzle
    solution = []
    for phase in range(2):
        print('phase', phase, 'depth', end=' ',flush=True)
        strt = time()
        cnt = 0
        blacklist = set([])
        for depth in range(30):
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
                print('cnt', cnt)
                break

cnt = 0
blacklist = set([])

move_ce_phase0 = [[] for _ in range(735471)]
with open('move/ce_phase0.csv', mode='r') as f:
    for idx in range(735471):
        move_ce_phase0[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ce_phase1_fbud = [[] for _ in range(12870)]
with open('move/ce_phase1_fbud.csv', mode='r') as f:
    for idx in range(12870):
        move_ce_phase1_fbud[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ce_phase1_rl = [[] for _ in range(70)]
with open('move/ce_phase1_rl.csv', mode='r') as f:
    for idx in range(70):
        move_ce_phase1_rl[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ep_phase1 = [[] for _ in range(2704156)]
with open('move/move_ep_phase1.csv', mode='r') as f:
    for idx in range(2704156):
        move_ep_phase1[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]


prunning = [None for _ in range(6)]
prun_len = [1, 2, 3, 2, 2, 3]
for phase in range(2):
    prunning[phase] = [[] for _ in range(prun_len[phase])]
    with open('prun/prunning' + str(phase) + '.csv', mode='r') as f:
        for lin in range(prun_len[phase]):
            prunning[phase][lin] = [int(i) for i in f.readline().replace('\n', '').split(',')]
solution = []
path = []
scramble = [move_candidate.index(i) for i in input("scramble: ").split()]
puzzle = Cube()
for mov in scramble:
    puzzle = puzzle.move(mov)
strt = time()
solver()
print('solution:',end=' ')
#print(solution)
for i in solution:
    print(move_candidate[i],end=' ')
print('')
print(len(solution), 'moves')
print(time() - strt, 'sec')
