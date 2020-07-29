'''
Solver:
* "X" twist includes X, X2, X', while "X2" means only X2
--- Reduction phase ---
phase 0: gather RL centers on RL faces
         use R, Rw, L, U, Uw, D, F, Fw, B
phase 1: gather FB centers on FB faces, separate low & high edges, clear RL center parity, avoid last two edges (= OLL Parity)
         use R, Rw, L, U, Uw2, D, F, Fw2, B
phase 2: make center columns and pair up 4 edges on the middle layer
         use R2, Rw2, L2, U, Uw2, D, F, Fw2, B
phase 3: complete center, edge pairing and clear edge parity (= PLL Parity), which means complete reduction
         use R2, Rw2, L2, U, Uw2, D, F2, Fw2, B2
--- 3x3x3 phase ---
phase 4: gather UD stickers on UD faces and clear EO
         use U, D, F, B, not use F2, B2
phase 5: solve it!
         use R2, L2, U, D, F2, B2
'''


from cube_class import Cube, face, axis, wide, move_cp, move_co, move_ep, move_ce, move_candidate, twist_to_idx, successor, ep_switch_parity, idx_ep_phase1, idx_ep_phase2, ec_parity
from time import time
from math import sqrt

def initialize_puzzle_arr(phase, puzzle):
    if phase == 0:
        return [puzzle.idx_ce_phase0()]
    elif phase == 1:
        return [puzzle.idx_ce_phase1_fbud() * 70 + puzzle.idx_ce_phase1_rl(), idx_ep_phase1(puzzle.Ep)]
    elif phase == 2:
        return [puzzle.idx_ce_phase23(), puzzle.Ep]
    elif phase == 3:
        return [puzzle.idx_ce_phase23(), puzzle.idx_ep_phase3()]
        #elif phase == 4:
        #return [puzzle.Cp, puzzle.Ep]
    elif phase == 4:
        return [puzzle.idx_co(), puzzle.idx_ep_phase4()]
    elif phase == 5:
        return [puzzle.idx_cp(), puzzle.idx_ep_phase5()]

def move_arr(puzzle_arr, phase, twist):
    if phase == 0:
        return [move_ce_phase0[puzzle_arr[0]][twist_to_idx[twist]]]
    elif phase == 1:
        return [move_ce_phase1_fbud[puzzle_arr[0] // 70][twist_to_idx[twist]] * 70 + move_ce_phase1_rl[puzzle_arr[0] % 70][twist_to_idx[twist]], move_ep_phase1[puzzle_arr[1]][twist_to_idx[twist]]]
    elif phase == 2:
        return [move_ce_phase23[puzzle_arr[0]][twist_to_idx[twist]], move_ep(puzzle_arr[1], twist)]
    elif phase == 3:
        return [move_ce_phase23[puzzle_arr[0]][twist_to_idx[twist]], move_ep_phase3[puzzle_arr[1]][twist_to_idx[twist]]]
        #elif phase == 4:
        #return [move_cp(puzzle_arr[0], twist), move_ep(puzzle_arr[1], twist)]
    elif phase == 4:
        return [move_co_arr[puzzle_arr[0]][twist_to_idx[twist]], move_ep_phase4[puzzle_arr[1]][twist_to_idx[twist]]]
    elif phase == 5:
        return [move_cp_arr[puzzle_arr[0]][twist_to_idx[twist]], move_ep_phase5_ud[puzzle_arr[1] // 24][twist_to_idx[twist]] * 24 + move_ep_phase5_fbrl[puzzle_arr[1] % 24][twist_to_idx[twist]]]

def distance(puzzle_arr, phase):
    global parity_cnt
    #if phase == 4:
    #    return 0#int(ec_parity([puzzle_arr[1][i] for i in range(0, 24, 2)], puzzle_arr[0]))
    if phase == 2:
        lst = [prunning[phase][0][puzzle_arr[0]], None, None]
        idxes = idx_ep_phase2(puzzle_arr[1])
        for i in range(2):
            lst[i + 1] = prunning[phase][i + 1][idxes[i]]
    else:
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
    ratio2 = pow(2, shift2 - sm)
    res = int((sm * ratio1 + mx * ratio2) / (ratio1 + ratio2))
    #res = int(sm)
    #print(mx, sm, ratio1, ratio2, res)
    
    if res == 0:
        puzzle_ep = [i for i in puzzle.Ep]
        for i in path:
            puzzle_ep = move_ep(puzzle_ep, i)
        if phase == 1: # find OLL Parity
            if ep_switch_parity(puzzle_ep):
                parity_cnt += 1
                return 99
        elif phase == 3: # find PLL Parity
            puzzle_ep = [puzzle_ep[i] // 2 for i in range(0, 24, 2)]
            puzzle_cp = [i for i in puzzle.Cp]
            for i in path:
                puzzle_cp = move_cp(puzzle_cp, i)
            if ec_parity(puzzle_ep, puzzle_cp):
                parity_cnt += 1
                return 99
    return res

skip_axis = [
    [3, 3, 3, 6, 6, 6, 9, 9, 9, 12, 12, 12, 15, 15, 15, 18, 18, 18, 21, 21, 21, 24, 24, 24, 27, 27, 27], # phase0
    [3, 3, 3, 6, 6, 6, 9, 9, 9, 12, 12, 12, 13, 16, 16, 16, 19, 19, 19, 20, 23, 23, 23], # phase1
    [1, 2, 3, 6, 6, 6, 7, 10, 10, 10, 13, 13, 13, 14, 17, 17, 17], # phase2
    [1, 2, 3, 6, 6, 6, 9, 9, 9, 10, 11, 12], # phase3
    # [2, 2, 4, 4, 7, 7, 7, 10, 10, 10, 12, 12, 14, 14], # phase4
    [1, 2, 5, 5, 5, 8, 8, 8, 10, 10, 12, 12], # phase4
    [1, 2, 5, 5, 5, 8, 8, 8, 9, 10] # phase5
    ]

def phase_search(phase, puzzle_arr, depth, dis):
    global path, cnt
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
            if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
                twist_idx = skip_axis[phase][twist_idx - 1]
                continue
            cnt += 1
            n_puzzle_arr = move_arr(puzzle_arr, phase, twist)
            path.append(twist)
            n_dis = distance(n_puzzle_arr, phase)
            if n_dis >= depth:
                path.pop()
                if n_dis > depth:
                    twist_idx = skip_axis[phase][twist_idx - 1]
                    if n_dis == 99:
                        return False
                continue
            if phase_search(phase, n_puzzle_arr, depth - 1, n_dis):
                return True
            path.pop()
        return False

def solver():
    global solution, path, cnt, puzzle, parity_cnt
    solution = []
    for phase in range(6):
        print('phase', phase, 'depth', end=' ',flush=True)
        strt = time()
        cnt = 0
        parity_cnt = 0
        for depth in range(40):
            print(depth, end=' ', flush=True)
            path = []
            puzzle_arr = initialize_puzzle_arr(phase, puzzle)
            dis = distance(puzzle_arr, phase)
            if phase_search(phase, puzzle_arr, depth, dis):
                for twist in path:
                    puzzle = puzzle.move(twist)
                solution.extend(path)
                print('')
                for i in path:
                    print(move_candidate[i], end=' ')
                print('')
                print(time() - strt, 'sec')
                print('cnt', cnt)
                print('parity', parity_cnt)
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
with open('move/ep_phase1.csv', mode='r') as f:
    for idx in range(2704156):
        move_ep_phase1[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ce_phase23 = [[] for _ in range(343000)]
with open('move/ce_phase23.csv', mode='r') as f:
    for idx in range(343000):
        move_ce_phase23[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ep_phase3 = [[] for _ in range(40320)]
with open('move/ep_phase3.csv', mode='r') as f:
    for idx in range(40320):
        move_ep_phase3[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_co_arr = [[] for _ in range(2187)]
with open('move/co.csv', mode='r') as f:
    for idx in range(2187):
        move_co_arr[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ep_phase4 = [[] for _ in range(495)]
with open('move/ep_phase4.csv', mode='r') as f:
    for idx in range(495):
        move_ep_phase4[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_cp_arr = [[] for _ in range(40320)]
with open('move/cp.csv', mode='r') as f:
    for idx in range(40320):
        move_cp_arr[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ep_phase5_ud = [[] for _ in range(40320)]
with open('move/ep_phase5_ud.csv', mode='r') as f:
    for idx in range(40320):
        move_ep_phase5_ud[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ep_phase5_fbrl = [[] for _ in range(24)]
with open('move/ep_phase5_fbrl.csv', mode='r') as f:
    for idx in range(24):
        move_ep_phase5_fbrl[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]


parity_cnt = 0

prunning = [None for _ in range(7)]
prun_len = [1, 2, 3, 2, 2, 2]
for phase in range(6):
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
    print('')
