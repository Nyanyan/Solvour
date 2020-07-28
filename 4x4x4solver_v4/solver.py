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
        #return move_ce_phase1_fbud[puzzle_arr // 70][twist_to_idx[twist]] * 70 + move_ce_phase1_rl[puzzle_arr % 70][twist_to_idx[twist]]

def distance(puzzle_arr, phase):
    lst = [prunning[phase][i][puzzle_arr[i]] for i in range(prun_len[phase])]
    #res = prunning[phase][puzzle_arr]
    '''
    mean = sum(lst) / prun_len[phase]
    sd_sum = 0
    for i in range(prun_len[phase]):
        sd_sum += pow(lst[i] - mean, 2)
    sd_sum = sqrt(sd_sum)
    sm = mean + sd_sum
    '''
    sm = sum(lst)
    #sm = sqrt(sum([i ** 2 for i in lst]))
    mx = max(lst)
    shift1 = 2
    ratio1 = pow(2, mx - shift1)
    shift2 = 3
    ratio2 = pow(3, shift2 - sm)
    res = int((sm * ratio1 + mx * ratio2) / (ratio1 + ratio2))
    #res = int(sm)
    #print(mx, sm, ratio1, ratio2, res)
    
    if res == 0 and phase == 1:
        puzzle_ep = [i for i in puzzle.Ep]
        for i in path:
            puzzle_ep = move_ep(puzzle_ep, i)
        '''
        for i in range(0, 24, 2):
            if puzzle_ep[i] % 2:
                return 99
        '''
        if ep_switch_parity(puzzle_ep):
            print('a', end='')
            return 99
    return res

skip_axis = [
    [3, 3, 3, 6, 6, 6, 9, 9, 9, 12, 12, 12, 15, 15, 15, 18, 18, 18, 21, 21, 21, 24, 24, 24, 27, 27, 27], 
    [3, 3, 3, 6, 6, 6, 9, 9, 9, 12, 12, 12, 13, 16, 16, 16, 19, 19, 19, 20, 23, 23, 23]
    ]

def phase_search(phase, puzzle_arr, depth):
    global path, cnt, blacklist
    dis = distance(puzzle_arr, phase)
    if depth == 0:
        return dis == 0
    else:
        l1_twist = path[-1] if len(path) >= 1 else -10
        l2_twist = path[-2] if len(path) >= 2 else -10
        l3_twist = path[-3] if len(path) >= 3 else -10
        twist_idx = 0
        while twist_idx < len(successor[phase]):
            twist = successor[phase][twist_idx]
            twist_idx += 1
            if (len(path) == 0 and face(twist) in blacklist) or face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
                twist_idx = skip_axis[phase][twist_idx - 1]
                continue
            cnt += 1
            n_puzzle_arr = move_arr(puzzle_arr, phase, twist)
            n_dis = distance(n_puzzle_arr, phase)
            if n_dis >= depth:
                if n_dis > depth:
                    twist_idx = skip_axis[phase][twist_idx - 1]
                    if n_dis == 99:
                        blacklist.add(face(path[0]))
                        return None
                continue
            path.append(twist)
            tmp = phase_search(phase, n_puzzle_arr, depth - 1)
            if tmp == None and len(path) - 1:
                return None
            if tmp:
                return True
            path.pop()
        return False

def solver():
    global solution, path, cnt, puzzle, blacklist
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

blacklist = set([])

prunning = [None for _ in range(6)]
prun_len = [1, 2, 3, 2, 2, 3]
for phase in range(2):
    prunning[phase] = [[] for _ in range(prun_len[phase])]
    with open('prun/prunning' + str(phase) + '.csv', mode='r') as f:
        for lin in range(prun_len[phase]):
            prunning[phase][lin] = [int(i) for i in f.readline().replace('\n', '').split(',')]
        #prunning[phase] = [int(i) for i in f.readline().replace('\n', '').split(',')]
while True:
    solution = []
    path = []
    cnt = 0
    inpt = [i for i in input("scramble: ").split()]
    if inpt[0] == 'exit':
        exit()
    scramble = [move_candidate.index(i) for i in inpt]
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
