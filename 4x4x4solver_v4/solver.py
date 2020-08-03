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

from cube_class import Cube, face, axis, wide, move_cp, move_co, move_ep, move_ce, move_candidate, twist_to_idx, successor, ep_switch_parity, idx_ep_phase1, idx_ep_phase2, ec_parity, ec_0_parity, skip_axis, reverse_move
from time import time
import numpy as np
from math import sqrt

import urllib.request
import csv
import os

def initialize_puzzle_arr(phase, puzzle):
    if phase == 0:
        return [puzzle.idx_ce_phase0()]
    elif phase == 1:
        return [puzzle.idx_ce_phase1_fbud() * 70 + puzzle.idx_ce_phase1_rl(), idx_ep_phase1(puzzle.Ep)]
        #return [puzzle.idx_ce_phase1_fbud() * 70 + puzzle.idx_ce_phase1_rl()]
    elif phase == 2:
        return [puzzle.idx_ce_phase23(), puzzle.Ep]
    elif phase == 3:
        return [puzzle.idx_ce_phase23(), puzzle.idx_ep_phase3()]
    elif phase == 4:
        return [puzzle.idx_co(), puzzle.idx_ep_phase4()]
    elif phase == 5:
        return [puzzle.idx_cp(), puzzle.idx_ep_phase5()]

def move_arr(puzzle_arr, phase, twist):
    if phase == 0:
        return [move_ce_phase0[puzzle_arr[0]][twist_to_idx[twist]]]
    elif phase == 1:
        #return [move_ce_phase1_fbud[puzzle_arr[0] // 70][twist_to_idx[twist]] * 70 + move_ce_phase1_rl[puzzle_arr[0] % 70][twist_to_idx[twist]]]
        return [move_ce_phase1_fbud[puzzle_arr[0] // 70][twist_to_idx[twist]] * 70 + move_ce_phase1_rl[puzzle_arr[0] % 70][twist_to_idx[twist]], move_ep_phase1[puzzle_arr[1]][twist_to_idx[twist]]]
    elif phase == 2:
        return [move_ce_phase23[puzzle_arr[0]][twist_to_idx[twist]], move_ep(puzzle_arr[1], twist)]
    elif phase == 3:
        return [move_ce_phase23[puzzle_arr[0]][twist_to_idx[twist]], move_ep_phase3[puzzle_arr[1]][twist_to_idx[twist]]]
    elif phase == 4:
        return [move_co_arr[puzzle_arr[0]][twist_to_idx[twist]], move_ep_phase4[puzzle_arr[1]][twist_to_idx[twist]]]
    elif phase == 5:
        return [move_cp_arr[puzzle_arr[0]][twist_to_idx[twist]], move_ep_phase5_ud[puzzle_arr[1] // 24][twist_to_idx[twist]] * 24 + move_ep_phase5_fbrl[puzzle_arr[1] % 24][twist_to_idx[twist]]]

def nyanyan_function(lst, phase):
    sm = sum(lst)
    mx = max(lst)
    mean = sm / len(lst)
    sd = 0
    for i in lst:
        sd += (mean - i) ** 2
    sd = sqrt(sd)
    #if phase == 5:
    return int(mx + sd)
    '''
    ratio = (5 * max(0, mx - 3) + sd) / 18 # ratio is small when mx is small and sd is small
    return int(mx * (1 - ratio) + sm * ratio)
    '''

def distance(puzzle_arr, phase):
    global parity_cnt
    if phase == 2:
        lst = [prunning[phase][0][puzzle_arr[0]], None, None]
        idxes = idx_ep_phase2(puzzle_arr[1])
        for i in range(2):
            lst[i + 1] = prunning[phase][i + 1][idxes[i]]
    else:
        lst = [prunning[phase][i][puzzle_arr[i]] for i in range(prun_len[phase])]
    res = nyanyan_function(lst, phase)
    if res == 0:
        puzzle_ep = [i for i in puzzle.Ep]
        puzzle_cp = [i for i in puzzle.Cp]
        for i in path:
            puzzle_ep = move_ep(puzzle_ep, i)
            puzzle_cp = move_cp(puzzle_cp, i)
        if phase == 1: # find OLL Parity (2 edge remaining)
            if ep_switch_parity(puzzle_ep):
                parity_cnt += 1
                return 99
        elif phase == 3: # find PLL Parity
            puzzle_ep = [puzzle_ep[i] // 2 for i in range(0, 24, 2)]
            if ec_parity(puzzle_ep, puzzle_cp):
                parity_cnt += 1
                return 99
        elif phase == 4:
            puzzle_ep = [puzzle_ep[i] // 2 for i in range(0, 24, 2)]
            if ec_0_parity(puzzle_ep, puzzle_cp):
                parity_cnt += 1
                return 99
    return res

def skip(phase, twist, l1_twist, l2_twist, l3_twist):
    if axis(twist) == axis(l1_twist) and face(twist) <= face(l1_twist):
        return True
    if phase < 4:
        if axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and face(twist) == face(l2_twist)):
            return True
    elif phase >= 4:
        if axis(twist) == axis(l1_twist) == axis(l2_twist):
            return True
    return False

def phase_search(phase, puzzle_arr, depth, dis):
    global path, cnt
    if depth == 0:
        return dis == 0
    else:
        if dis == 0:
            return False
        l1_twist = path[-1] if len(path) >= 1 else -10
        l2_twist = path[-2] if len(path) >= 2 else -10
        l3_twist = path[-3] if len(path) >= 3 else -10
        twist_idx = 0
        '''
        if phase == 1:
            n_dises = [[99, [], i] for i in range(len(successor[phase]))]
        '''
        while twist_idx < len(successor[phase]):
            twist = successor[phase][twist_idx]
            if skip(phase, twist, l1_twist, l2_twist, l3_twist):
                twist_idx = skip_axis[phase][twist_idx]
                continue
            cnt += 1
            n_puzzle_arr = move_arr(puzzle_arr, phase, twist)
            #if phase != 1:
            path.append(twist)
            n_dis = distance(n_puzzle_arr, phase)
            if n_dis >= depth:
                #if phase != 1:
                path.pop()
                if n_dis > depth:
                    twist_idx = skip_axis[phase][twist_idx]
                    if n_dis == 99:
                        return False
                else:
                    twist_idx += 1
                continue
            #print(dis, n_dis)
            #if phase != 1:
            if phase_search(phase, n_puzzle_arr, depth - 1, n_dis):
                return True
            path.pop()
            '''
            else:
                n_dises[twist_idx][0] = n_dis
                n_dises[twist_idx][1] = n_puzzle_arr
            '''
            twist_idx += 1
        '''
        if phase == 1:
            n_dises.sort()
            for i in range(len(successor[phase])):
                if n_dises[i][0] == 99:
                    return False
                twist_idx = n_dises[i][2]
                path.append(successor[phase][twist_idx])
                if phase_search(phase, n_dises[i][1], depth - 1, n_dises[i][0]):
                    return True
                path.pop()
        '''
        return False

def solver():
    global path, cnt, puzzle, parity_cnt
    strt_all = time()
    solution = []
    part_3_max_depth = 30
    #max_depth = [20, 20, 20, 20, part_3_max_depth, 0]
    #strt_depth = [0, 0, 0, 0, 0, 0]
    phase = 0
    #phase4_path = []
    analytics = [[-1 for _ in range(7)] for _ in range(2)]
    while phase < 6:
        strt = time()
        cnt = 0
        parity_cnt = 0
        puzzle_arr = initialize_puzzle_arr(phase, puzzle)
        dis = distance(puzzle_arr, phase)
        depth = dis #strt_depth[phase]
        print('phase', phase, 'depth', end=' ',flush=True)
        while depth < 30: #max_depth[phase]:
            print(depth, end=' ', flush=True)
            path = []
            if phase_search(phase, puzzle_arr, depth, dis):
                for twist in path:
                    puzzle = puzzle.move(twist)
                solution.extend(path)
                phase_time = time() - strt

                print('')
                for i in path:
                    print(move_candidate[i], end=' ')
                print('')
                print(phase_time, 'sec')
                print('cnt', cnt)
                print('parity', parity_cnt)
                
                analytics[0][phase] = depth
                analytics[1][phase] = phase_time
                '''
                if phase == 4:
                    phase4_path = [i for i in path]
                    max_depth[5] = part_3_max_depth - depth
                '''
                phase += 1
                break
            depth += 1
        else:
            print('failed!')
            '''
            if phase == 5:
                print('phase5 failed. go back to phase 4')
                strt_depth[4] = part_3_max_depth - max_depth[5] + 1
                phase = 4
                for i in reverse_move(phase4_path):
                    solution.pop()
                    puzzle = puzzle.move(i)
            '''
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

print('getting moving array')
move_ce_phase0 = np.zeros((735471, 27), dtype=np.int)
with open('move/ce_phase0.csv', mode='r') as f:
    for idx in range(735471):
        move_ce_phase0[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
print('.',end='',flush=True)
move_ce_phase1_fbud = [[] for _ in range(12870)]
with open('move/ce_phase1_fbud.csv', mode='r') as f:
    for idx in range(12870):
        move_ce_phase1_fbud[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
print('.',end='',flush=True)
move_ce_phase1_rl = [[] for _ in range(70)]
with open('move/ce_phase1_rl.csv', mode='r') as f:
    for idx in range(70):
        move_ce_phase1_rl[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
print('.',end='',flush=True)
move_ep_phase1 = np.zeros((2704156, 27), dtype=np.int)
with open('move/ep_phase1.csv', mode='r') as f:
    for idx in range(2704156):
        move_ep_phase1[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
print('.',end='',flush=True)
move_ce_phase23 = [[] for _ in range(343000)]
with open('move/ce_phase23.csv', mode='r') as f:
    for idx in range(343000):
        move_ce_phase23[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
print('.',end='',flush=True)
move_ep_phase3 = [[] for _ in range(40320)]
with open('move/ep_phase3.csv', mode='r') as f:
    for idx in range(40320):
        move_ep_phase3[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
print('.',end='',flush=True)
move_co_arr = [[] for _ in range(2187)]
with open('move/co.csv', mode='r') as f:
    for idx in range(2187):
        move_co_arr[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
print('.',end='',flush=True)
move_ep_phase4 = [[] for _ in range(495)]
with open('move/ep_phase4.csv', mode='r') as f:
    for idx in range(495):
        move_ep_phase4[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
print('.',end='',flush=True)
move_cp_arr = [[] for _ in range(40320)]
with open('move/cp.csv', mode='r') as f:
    for idx in range(40320):
        move_cp_arr[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
print('.',end='',flush=True)
move_ep_phase5_ud = [[] for _ in range(40320)]
with open('move/ep_phase5_ud.csv', mode='r') as f:
    for idx in range(40320):
        move_ep_phase5_ud[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
print('.',end='',flush=True)
move_ep_phase5_fbrl = [[] for _ in range(24)]
with open('move/ep_phase5_fbrl.csv', mode='r') as f:
    for idx in range(24):
        move_ep_phase5_fbrl[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
print('.')
prunning = [None for _ in range(7)]
prun_len = [1, 2, 3, 2, 2, 2]
print('getting prunning array')
for phase in range(6):
    prunning[phase] = [[] for _ in range(prun_len[phase])]
    with open('prun/prunning' + str(phase) + '.csv', mode='r') as f:
        for lin in range(prun_len[phase]):
            prunning[phase][lin] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    print('.',end='',flush=True)
print('')
parity_cnt = 0
cnt = 0
puzzle = Cube()
path = []

def main():
    global puzzle
    for num in range(100):
        '''
        response = urllib.request.urlopen('http://localhost:2014/scramble/.txt?e=444')
        scramble = response.read().decode('utf8', 'ignore').rstrip(os.linesep)
        inpt = [i for i in scramble.split()]
        '''
        inpt = [i for i in input("scramble: ").split()]
        print(num)
        if inpt == []:
            exit()
        scramble = [move_candidate.index(i) for i in inpt]
        puzzle = Cube()
        for mov in scramble:
            puzzle = puzzle.move(mov)
        strt = time()
        solution = solver()
        print('solution:',end=' ')
        #print(solution)
        for i in solution:
            print(move_candidate[i],end=' ')
        print('')
        print(len(solution), 'moves')
        print(time() - strt, 'sec')
        print('')

if __name__ == '__main__':
    main()