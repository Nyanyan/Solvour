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
import concurrent.futures
import ray

@ray.remote
def initialize_puzzle_arr(phase, puzzle):
    if phase == 0:
        return [puzzle.idx_ce_phase0()]
    '''
    elif phase == 1:
        return [puzzle.idx_ce_phase1_fbud() * 70 + puzzle.idx_ce_phase1_rl(), idx_ep_phase1(puzzle.Ep)]
    elif phase == 2:
        res = [puzzle.idx_ce_phase23()]
        res.extend(puzzle.Ep)
        return res
    elif phase == 3:
        return [puzzle.idx_ce_phase23(), puzzle.idx_ep_phase3()]
    elif phase == 4:
        return [puzzle.idx_co(), puzzle.idx_ep_phase4()]
    elif phase == 5:
        return [puzzle.idx_cp(), puzzle.idx_ep_phase5()]
    '''

@ray.remote
def move_arr(puzzle_arr, phase, twist, move_ce_phase0):
    if phase == 0:
        return [move_ce_phase0[puzzle_arr[0]][twist_to_idx[twist]]]
    '''
    elif phase == 1:
        return [move_ce_phase1_fbud[puzzle_arr[0] // 70][twist_to_idx[twist]] * 70 + move_ce_phase1_rl[puzzle_arr[0] % 70][twist_to_idx[twist]], move_ep_phase1[puzzle_arr[1]][twist_to_idx[twist]]]
    elif phase == 2:
        return [move_ce_phase23[puzzle_arr[0]][twist_to_idx[twist]], move_ep(puzzle_arr[1:], twist)]
    elif phase == 3:
        return [move_ce_phase23[puzzle_arr[0]][twist_to_idx[twist]], move_ep_phase3[puzzle_arr[1]][twist_to_idx[twist]]]
    elif phase == 4:
        return [move_co_arr[puzzle_arr[0]][twist_to_idx[twist]], move_ep_phase4[puzzle_arr[1]][twist_to_idx[twist]]]
    elif phase == 5:
        return [move_cp_arr[puzzle_arr[0]][twist_to_idx[twist]], move_ep_phase5_ud[puzzle_arr[1] // 24][twist_to_idx[twist]] * 24 + move_ep_phase5_fbrl[puzzle_arr[1] % 24][twist_to_idx[twist]]]
    '''

def nyanyan_function(lst, phase):
    if phase == 5:
        return max(lst)
    else:
        sm = sum(lst)
        mx = max(lst)
        ratio = pow(2, max(mx - 5, mx * 2 - sm - 4)) # small when mx is small and sm neary equal to mx*2
        return int((mx + sm * ratio) / (1 + ratio))

@ray.remote
def distance(puzzle_arr, phase, first_twist_idx, prunning):
    #global parity_cnt
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
        for i in path[first_twist_idx]:
            puzzle_ep = move_ep(puzzle_ep, i)
            puzzle_cp = move_cp(puzzle_cp, i)
        if phase == 1: # find OLL Parity
            if ep_switch_parity(puzzle_ep):
                #parity_cnt += 1
                return 99
        elif phase == 3: # find PLL Parity
            puzzle_ep = [puzzle_ep[i] // 2 for i in range(0, 24, 2)]
            if ec_parity(puzzle_ep, puzzle_cp):
                #parity_cnt += 1
                return 99
        elif phase == 4:
            puzzle_ep = [puzzle_ep[i] // 2 for i in range(0, 24, 2)]
            if ec_0_parity(puzzle_ep, puzzle_cp):
                #parity_cnt += 1
                return 99
    return res

@ray.remote
def phase_search(phase, puzzle_arr, depth, dis, first_twist_idx, move_ce_phase0, prunning):
    global path, cnt, quit_flag
    if quit_flag:
        return False
    if depth == 0:
        if dis == 0:
            quit_flag = True
            return True
    else:
        l1_twist = path[first_twist_idx][-1] if len(path[first_twist_idx]) >= 1 else -10
        l2_twist = path[first_twist_idx][-2] if len(path[first_twist_idx]) >= 2 else -10
        l3_twist = path[first_twist_idx][-3] if len(path[first_twist_idx]) >= 3 else -10
        twist_idx = 0
        while twist_idx < len(successor[phase]):
            twist = successor[phase][twist_idx]
            twist_idx += 1
            if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1) or (axis(twist) == axis(l1_twist) == axis(l2_twist) and wide(twist) == wide(l1_twist) == wide(l2_twist) == 0):
                twist_idx = skip_axis[phase][twist_idx - 1]
                continue
            cnt += 1
            n_puzzle_arr = ray.get(move_arr.remote(puzzle_arr, phase, twist, move_ce_phase0))
            path[first_twist_idx].append(twist)
            n_dis = ray.get(distance.remote(n_puzzle_arr, phase, first_twist_idx, prunning))
            if n_dis >= depth:
                path[first_twist_idx].pop()
                if n_dis > depth:
                    twist_idx = skip_axis[phase][twist_idx - 1]
                    if n_dis == 99:
                        return False
                continue
            if ray.get(phase_search.remote(phase, n_puzzle_arr, depth - 1, n_dis, first_twist_idx)):
                return True
            path[first_twist_idx].pop()
        return False

@ray.remote
def phase_solver(phase, first_twist_idx, depth, puzzle_arr, move_ce_phase0, prunning):
    global path, cnt, puzzle, parity_cnt
    strt = time()
    path[first_twist_idx] = [successor[phase][first_twist_idx]]
    '''
    puzzle_tmp = puzzle.move(successor[phase][first_twist_idx])
    puzzle_arr = initialize_puzzle_arr(phase, puzzle_tmp)
    '''
    dis = ray.get(distance.remote(puzzle_arr, phase, first_twist_idx, prunning))
    if ray.get(phase_search.remote(phase, puzzle_arr, depth, dis, first_twist_idx, move_ce_phase0, prunning)):
        '''
        print('')
        print(time() - strt, 'sec', depth + 1, 'moves No', first_twist_idx, 'answer found', end=' ')
        for i in path[first_twist_idx]:
            print(move_candidate[i], end=' ')
        print('')
        '''
        return first_twist_idx
    return -1

def init():
    global move_ce_phase0, move_ce_phase1_fbud, move_ce_phase1_rl, move_ep_phase1, move_ce_phase23, move_ep_phase3, move_co_arr, move_ep_phase4, move_cp_arr, move_ep_phase5_ud, move_ep_phase5_fbrl, prunning, move_ce_phase0_id, prunning_id
    ray.init()
    print('getting moving array')
    move_ce_phase0 = np.zeros((735471, 27), dtype=np.int)
    '''
    move_ce_phase0_base = Array('i', 735471 * 27)
    move_ce_phase0 = np.ctypeslib.as_array(move_ce_phase0_base.get_obj())
    move_ce_phase0 = move_ce_phase0.reshape(735471, 27)
    '''
    with open('move/ce_phase0.csv', mode='r') as f:
        for idx in range(735471):
            move_ce_phase0[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    move_ce_phase0_id = ray.put(move_ce_phase0)
    '''
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
    '''
    #prunning = np.ctypeslib.as_array(prunning_base.get_obj())
    prunning = [None for _ in range(7)]
    #prun_max_idx = [[735471], [900970, 2704156], [343000, 665280, 665280], [343000, 40320], [2187, 495], [40320, 967704]]
    print('getting prunning array')
    for phase in range(1):
        prunning[phase] = [[] for i in range(prun_len[phase])]
        with open('prun/prunning' + str(phase) + '.csv', mode='r') as f:
            for lin in range(prun_len[phase]):
                prunning[phase][lin] = [int(i) for i in f.readline().replace('\n', '').split(',')]
        print('.',end='',flush=True)
    print('')
    prunning_id = ray.put(prunning)


move_ce_phase0 = None
move_ce_phase1_fbud = None
move_ce_phase1_rl = None
move_ep_phase1 = None
move_ce_phase23 = None
move_ep_phase3 = None
move_co_arr = None
move_ep_phase4 = None
move_cp_arr = None
move_ep_phase5_ud = None
move_ep_phase5_fbrl = None
prunning = None

move_ce_phase0_id = None
move_ce_phase1_fbud_id = None
move_ce_phase1_rl_id = None
move_ep_phase1_id = None
move_ce_phase23_id = None
move_ep_phase3_id = None
move_co_arr_id = None
move_ep_phase4_id = None
move_cp_arr_id = None
move_ep_phase5_ud_id = None
move_ep_phase5_fbrl_id = None
prunning_id = None

parity_cnt = 0
cnt = 0
puzzle = Cube()
path = [[] for _ in range(27)]
quit_flag = False
prun_len = [1, 2, 3, 2, 2, 2]

def main():
    global puzzle, path, quit_flag #, move_ce_phase0, move_ce_phase1_fbud, move_ce_phase1_rl, move_ep_phase1, move_ce_phase23, move_ep_phase3, move_co_arr, move_ep_phase4, move_cp_arr, move_ep_phase5_ud, move_ep_phase5_fbrl, prunning
    '''
    with Manager() as manager:
        move_ce_phase0 = manager.list(move_ce_phase0)
        move_ce_phase1_fbud = manager.list(move_ce_phase1_fbud)
        move_ce_phase1_rl = manager.list(move_ce_phase1_rl)
        move_ep_phase1 = manager.list(move_ep_phase1)
        move_ce_phase23 = manager.list(move_ce_phase23)
        move_ep_phase3 = manager.list(move_ep_phase3)
        move_co_arr = manager.list(move_co_arr)
        move_ep_phase4 = manager.list(move_ep_phase4)
        move_cp_arr = manager.list(move_cp_arr)
        move_ep_phase5_ud = manager.list(move_ep_phase5_ud)
        move_ep_phase5_fbrl = manager.list(move_ep_phase5_fbrl)
        prunning = manager.list(prunning)
    '''
    init()
    while True:
        inpt = [i for i in input("scramble: ").split()]
        if inpt[0] == 'exit':
            exit()
        scramble = [move_candidate.index(i) for i in inpt]
        puzzle = Cube()
        for mov in scramble:
            puzzle = puzzle.move(mov)
        solution = []
        all_strt = time()
        for phase in range(1):
            path = [[] for _ in range(len(successor[phase]))]
            puzzle_arr = ray.get(initialize_puzzle_arr.remote(phase, puzzle))
            dis = ray.get(distance.remote(puzzle_arr, phase, 0, prunning_id))
            print('phase', phase, 'depth 0', end=' ',flush=True)
            if dis == 0:
                print('skip')
                continue
            flag = False
            strt = time()
            for depth in range(20):
                print(depth + 1, end=' ', flush=True)
                quit_flag = False
<<<<<<< HEAD
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(phase_solver, phase, first_twist_idx, depth) for first_twist_idx in range(len(successor[phase]))]
                    for future in concurrent.futures.as_completed(futures):
                        tmp = future.result()
=======
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    '''
                    arg1 = [phase for first_twist_idx in range(len(successor[phase]))]
                    arg2 = [first_twist_idx for first_twist_idx in range(len(successor[phase]))]
                    arg3 = [depth for first_twist_idx in range(len(successor[phase]))]
                    executor.map(phase_solver, arg1, arg2, arg3, chunksize=1)
                    '''
                    fs = [phase_solver.remote(phase, first_twist_idx, depth, initialize_puzzle_arr.remote(phase, puzzle.move(successor[phase][first_twist_idx])), move_ce_phase0_id, prunning_id) for first_twist_idx in range(len(successor[phase]))]
                    #for future in concurrent.futures.as_completed(fs): # concurrent.futures.as_completed(futures)
                    #print(ray.get(fs))
                    for output in ray.get(fs):
                        #tmp = future.result()
                        tmp = output
>>>>>>> 2647eca610fcc8ffb196c770af8b8bd65b069616
                        if tmp != -1:
                            solution.extend(path[tmp])
                            print('')
                            print(time() - strt, 'sec', depth + 1, 'moves No', tmp, 'answer found', end=' ')
                            for i in path[tmp]:
                                puzzle = puzzle.move(i)
                                print(move_candidate[i], end=' ')
                            print('')
                            flag = True
                            break
                if flag:
                    break
        print('solution:',end=' ')
        #print(solution)
        for i in solution:
            print(move_candidate[i],end=' ')
        print('')
        print(len(solution), 'moves')
        print(time() - all_strt, 'sec')
        print('')

if __name__ == '__main__':
    main()