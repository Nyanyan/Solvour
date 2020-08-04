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
         use R2, L2, U, D, F, B, not use F2, B2
phase 5: solve it!
         use R2, L2, U, D, F2, B2
'''
from cube_class_c_4 import Cube, face, axis, wide, move_cp, move_co, move_ep, move_ce, move_candidate, twist_to_idx, successor, ep_switch_parity, idx_ep_phase1, idx_ep_phase2, ec_parity, ec_0_parity, skip_axis, reverse_move
from time import time
import numpy as np
from math import sqrt
import csv
cimport cython

cdef initialize_puzzle_arr(int phase, puzzle):
    if phase == 0:
        return [puzzle.idx_ce_phase0()]
    elif phase == 1:
        return [puzzle.idx_ce_phase1_fbud() * 70 + puzzle.idx_ce_phase1_rl(), idx_ep_phase1(puzzle.Ep)]
    elif phase == 2:
        return [puzzle.idx_ce_phase23(), puzzle.Ep]
    elif phase == 3:
        return [puzzle.idx_ce_phase23(), puzzle.idx_ep_phase3()]
    elif phase == 4:
        return [puzzle.idx_co(), puzzle.idx_ep_phase4()]
    elif phase == 5:
        return [puzzle.idx_cp(), puzzle.idx_ep_phase5()]

cdef move_arr(puzzle_arr, int phase, int twist):
    cdef int tmp = twist_to_idx[twist]
    if phase == 0:
        return [move_ce_phase0[puzzle_arr[0]][tmp]]
    elif phase == 1:
        return [move_ce_phase1_fbud[puzzle_arr[0] // 70][tmp] * 70 + move_ce_phase1_rl[puzzle_arr[0] % 70][tmp], move_ep_phase1[puzzle_arr[1]][tmp]]
    elif phase == 2:
        return [move_ce_phase23[puzzle_arr[0]][tmp], move_ep(puzzle_arr[1], twist)]
    elif phase == 3:
        return [move_ce_phase23[puzzle_arr[0]][tmp], move_ep_phase3[puzzle_arr[1]][tmp]]
    elif phase == 4:
        return [move_co_arr[puzzle_arr[0]][tmp], move_ep_phase4[puzzle_arr[1]][tmp]]
    elif phase == 5:
        return [move_cp_arr[puzzle_arr[0]][tmp], move_ep_phase5_ud[puzzle_arr[1] // 24][tmp] * 24 + move_ep_phase5_fbrl[puzzle_arr[1] % 24][tmp]]

cdef nyanyan_function(lst, int phase):
    cdef int sm = sum(lst)
    cdef int mx = max(lst)
    cdef float mean = sm / len(lst)
    cdef float sd = 0
    cdef int i
    for i in lst:
        sd += (mean - i) ** 2
    sd = sqrt(sd)
    cdef float euclid = 0
    for i in lst:
        euclid += i ** 2
    euclid = sqrt(euclid)
    #return int(l + sd)
    '''
    if phase == 5:
        return int(mx + sd)
    '''
    #ratio = min(1, max(0, mx + sd - 8) / 5) # ratio is small when mx is small and sd is small
    #return int(mx * (1 - ratio) + (l + sd) * ratio)
    cdef float ratio = min(1, (3 * max(0, mx - 5) + sd) / 7) # ratio is small when mx is small and sd is small
    return int(mx * (1 - ratio) + euclid * ratio)
    

cdef distance(puzzle_arr, int phase):
    #global parity_cnt
    if phase == 2:
        lst = [prunning[phase][0][puzzle_arr[0]], None, None]
        idxes = idx_ep_phase2(puzzle_arr[1])
        for i in range(2):
            lst[i + 1] = prunning[phase][i + 1][idxes[i]]
    else:
        lst = [prunning[phase][i][puzzle_arr[i]] for i in range(prun_len[phase])]
    cdef int res = nyanyan_function(lst, phase)
    cdef int[24] puzzle_ep
    cdef int[8] puzzle_cp
    cdef int[12] puzzle_ep_p
    if res == 0:
        puzzle_ep = [i for i in puzzle.Ep]
        puzzle_cp = [i for i in puzzle.Cp]
        for i in path:
            puzzle_ep = move_ep(puzzle_ep, i)
            puzzle_cp = move_cp(puzzle_cp, i)
        if phase == 1: # find OLL Parity (2 edge remaining)
            if ep_switch_parity(puzzle_ep):
                #parity_cnt += 1
                return 99
        elif phase == 3: # find PLL Parity
            puzzle_ep_p = [puzzle_ep[i] // 2 for i in range(0, 24, 2)]
            if ec_parity(puzzle_ep_p, puzzle_cp):
                #parity_cnt += 1
                return 99
        elif phase == 4:
            puzzle_ep_p = [puzzle_ep[i] // 2 for i in range(0, 24, 2)]
            if ec_0_parity(puzzle_ep_p, puzzle_cp):
                #parity_cnt += 1
                return 99
    return res

cdef skip(int phase, int twist, int l1_twist, int l2_twist, int l3_twist):
    cdef int axis_twist = axis(twist)
    cdef int axis_l1_twist = axis(l1_twist)
    cdef int face_twist = face(twist)
    if axis_twist == axis_l1_twist and face_twist <= face(l1_twist):
        return True
    if phase < 4:
        if axis_twist == axis_l1_twist == axis(l2_twist) == axis(l3_twist) or (axis_twist == axis_l1_twist and face_twist == face(l2_twist)):
            return True
    elif phase >= 4:
        if axis_twist == axis_l1_twist == axis(l2_twist):
            return True
    return False

cdef phase_search(int phase, puzzle_arr, int depth, int dis):
    global path, cnt
    cdef int l1_twist, l2_twist, l3_twist, twist_idx, len_successor, n_dis, twist
    if depth == 0:
        return dis == 0
    else:
        if dis == 0:
            return True
        l1_twist = path[-1] if len(path) >= 1 else -10
        l2_twist = path[-2] if len(path) >= 2 else -10
        l3_twist = path[-3] if len(path) >= 3 else -10
        twist_idx = 0
        len_successor = len(successor[phase])
        for _ in range(27):
            if twist_idx >= len_successor:
                return False
            twist = successor[phase][twist_idx]
            if skip(phase, twist, l1_twist, l2_twist, l3_twist):
                twist_idx = skip_axis[phase][twist_idx]
                continue
            #cnt += 1
            n_puzzle_arr = move_arr(puzzle_arr, phase, twist)
            path.append(twist)
            n_dis = distance(n_puzzle_arr, phase)
            if n_dis >= depth:
                path.pop()
                if n_dis > depth:
                    twist_idx = skip_axis[phase][twist_idx]
                    if n_dis == 99:
                        return False
                else:
                    twist_idx += 1
                continue
            if phase_search(phase, n_puzzle_arr, depth - 1, n_dis):
                return True
            path.pop()
            twist_idx += 1

def solver(p):
    global path, cnt, puzzle, parity_cnt, puzzle
    puzzle = p
    strt_all = time()
    solution = []
    #part_3_max_depth = 30
    cdef int phase = 0
    analytics = [[-1 for _ in range(7)] for _ in range(2)]
    cdef int dis, depth, twist
    while phase < 6:
        strt = time()
        #cnt = 0
        #parity_cnt = 0
        puzzle_arr = initialize_puzzle_arr(phase, puzzle)
        dis = distance(puzzle_arr, phase)
        depth = dis
        #print('phase', phase, 'depth', end=' ',flush=True)
        while depth < 30: #max_depth[phase]:
            #print(depth, end=' ', flush=True)
            path = []
            if phase_search(phase, puzzle_arr, depth, dis):
                for twist in path:
                    puzzle = puzzle.move(twist)
                solution.extend(path)
                phase_time = time() - strt
                '''
                print('')
                for i in path:
                    print(move_candidate[i], end=' ')
                print('')
                
                print(len(path))
                print(phase_time, 'sec')
                print('cnt', cnt)
                print('parity', parity_cnt)
                '''
                analytics[0][phase] = depth
                analytics[1][phase] = phase_time
                phase += 1
                break
            depth += 1
        else:
            print('failed!')
    all_time = time() - strt_all
    analytics[0][6] = len(solution)
    analytics[1][6] = all_time
    with open('analytics_len.csv', mode='a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(analytics[0])
    with open('analytics_time.csv', mode='a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(analytics[1])
    return solution

move_ce_phase0 = np.zeros((735471, 27), dtype=np.int)
move_ce_phase1_fbud = [[] for _ in range(12870)]
move_ce_phase1_rl = [[] for _ in range(70)]
move_ep_phase1 = np.zeros((2704156, 27), dtype=np.int)
move_ce_phase23 = [[] for _ in range(343000)]
move_ep_phase3 = [[] for _ in range(40320)]
move_co_arr = [[] for _ in range(2187)]
move_ep_phase4 = [[] for _ in range(495)]
move_cp_arr = [[] for _ in range(40320)]
move_ep_phase5_ud = [[] for _ in range(40320)]
move_ep_phase5_fbrl = [[] for _ in range(24)]
prunning = [None for _ in range(7)]
prun_len = [1, 2, 3, 2, 2, 2]

if __name__ == 'solver_c_10':
    global move_ce_phase0, move_ce_phase1_fbud, move_ce_phase1_rl, move_ep_phase1, move_ce_phase23, move_ep_phase3, move_co_arr, move_ep_phase4, move_cp_arr, move_ep_phase5_ud, move_ep_phase5_fbrl, prunning, prun_len
    print('getting moving array')
    with open('move/ce_phase0.csv', mode='r') as f:
        for idx in range(735471):
            move_ce_phase0[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ce_phase1_fbud.csv', mode='r') as f:
        for idx in range(12870):
            move_ce_phase1_fbud[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ce_phase1_rl.csv', mode='r') as f:
        for idx in range(70):
            move_ce_phase1_rl[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ep_phase1.csv', mode='r') as f:
        for idx in range(2704156):
            move_ep_phase1[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ce_phase23.csv', mode='r') as f:
        for idx in range(343000):
            move_ce_phase23[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ep_phase3.csv', mode='r') as f:
        for idx in range(40320):
            move_ep_phase3[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/co.csv', mode='r') as f:
        for idx in range(2187):
            move_co_arr[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ep_phase4.csv', mode='r') as f:
        for idx in range(495):
            move_ep_phase4[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/cp.csv', mode='r') as f:
        for idx in range(40320):
            move_cp_arr[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ep_phase5_ud.csv', mode='r') as f:
        for idx in range(40320):
            move_ep_phase5_ud[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ep_phase5_fbrl.csv', mode='r') as f:
        for idx in range(24):
            move_ep_phase5_fbrl[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.')
    print('getting prunning array')
    for phase in range(6):
        prunning[phase] = [[] for _ in range(prun_len[phase])]
        with open('prun/prunning' + str(phase) + '.csv', mode='r') as f:
            for lin in range(prun_len[phase]):
                prunning[phase][lin] = [int(i) for i in f.readline().replace('\n', '').split(',')]
        #print('.',end='',flush=True)
    #print('')
cdef int parity_cnt = 0
cdef int cnt = 0
puzzle = Cube()
path = []
