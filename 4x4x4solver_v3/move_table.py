from cube_class import Cube, face
from collections import deque
import csv
##                  0    1     2     3     4      5      6    7     8     9     10     11     12   13    14    15    16     17     18   19   20     21    22     23     24   25    26    27    28     29     30   31    32    33    34     35
#move_candidate = ["R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "Lw", "Lw2", "Lw'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "Dw", "Dw2", "Dw'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'", "Bw", "Bw2", "Bw'"]

move_arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24, 25, 26, 27, 28, 29, 30, 31, 32]
twist_to_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, -1, -1, -1, 9, 10, 11, 12, 13, 14, 15, 16, 17, -1, -1, -1, 18, 19, 20, 21, 22, 23, 24, 25, 26, -1, -1, -1]

solved = Cube()
'''
cp_move = [[-1 for _ in range(len(move_arr))] for _ in range(40320)]
que = deque([solved])
cnt = 0
print('CP move index')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_cp()
    if cp_move[idx][0] == -1:
        for twist in move_arr:
            n_puzzle = puzzle.move(twist)
            n_idx = n_puzzle.idx_cp()
            cp_move[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move_table/move_cp.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in cp_move:
        writer.writerow(arr)


co_move = [[-1 for _ in range(len(move_arr))] for _ in range(2187)]
que = deque([solved])
cnt = 0
print('CO move index')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_co()
    if co_move[idx][0] == -1:
        for twist in move_arr:
            n_puzzle = puzzle.move(twist)
            n_idx = n_puzzle.idx_co()
            co_move[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move_table/move_co.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in co_move:
        writer.writerow(arr)


ce_move_phase0 = [[-1 for _ in range(len(move_arr))] for _ in range(735471)]
que = deque([solved])
cnt = 0
print('CE move index phase0')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_ce_phase0()
    #print(idx)
    if ce_move_phase0[idx][0] == -1:
        for twist in move_arr:
            n_puzzle = puzzle.move(twist)
            n_idx = n_puzzle.idx_ce_phase0()
            ce_move_phase0[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move_table/move_ce_phase0.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ce_move_phase0:
        writer.writerow(arr)


ce_move_phase1_fbud = [[-1 for _ in range(len(move_arr))] for _ in range(12870)]
que = deque([solved])
cnt = 0
print('CE move index phase1 FBUD')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_ce_phase1_fbud()
    if ce_move_phase1_fbud[idx][0] == -1:
        for twist in move_arr:
            n_puzzle = puzzle.move(twist)
            n_idx = n_puzzle.idx_ce_phase1_fbud()
            ce_move_phase1_fbud[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move_table/move_ce_phase1_fbud.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ce_move_phase1_fbud:
        writer.writerow(arr)


ce_move_phase1_rl = [[-1 for _ in range(len(move_arr))] for _ in range(70)]
que = deque([solved])
cnt = 0
print('CE move index phase1 RL')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_ce_phase1_rl()
    if ce_move_phase1_rl[idx][0] == -1:
        for twist in move_arr:
            n_puzzle = puzzle.move(twist)
            n_idx = n_puzzle.idx_ce_phase1_rl()
            ce_move_phase1_rl[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move_table/move_ce_phase1_rl.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ce_move_phase1_rl:
        writer.writerow(arr)
'''



decision = [[[], [], [2, 3, 6, 7], [18, 19, 22, 23], [11, 10, 9, 8], [15, 14, 13, 12]], [[12, 13, 10, 11], [8, 9, 14, 15], [0, 1, 4, 5], [16, 17, 20, 21], [], []],[[3, 2, 19, 18], [7, 6, 23, 22], [], [], [5, 4, 17, 16], [1, 0, 21, 20]]]
ep_move_phase1 = [[[[-1 for _ in range(16)] for _ in range(len(move_arr))] for _ in range(256)] for _ in range(3)]
que = deque([solved])
cnt = 0
print('EP move index phase1')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
        #print(ep_move_phase1[1][0][0])
    puzzle = que.popleft()
    idxes = puzzle.idx_high_low_edge()
    for twist in move_arr:
        n_puzzle = puzzle.move(twist)
        #print(n_puzzle.Ep)
        #print(n_puzzle.Ep)
        n_idxes = n_puzzle.idx_high_low_edge()
        #print(n_idxes)
        flag = False
        for mse in range(3):
            decision_arr = [int(puzzle.Ep[i] % 2 != i % 2) for i in decision[mse][twist // 6]]
            decision_num = 0
            for i in decision_arr:
                decision_num *= 2
                decision_num += i
            #print(decision_arr, decision_num, [n_puzzle.Ep[i] for i in decision[mse][twist // 6]], decision[mse][twist // 6])
            if ep_move_phase1[mse][idxes[mse]][twist_to_idx[twist]][decision_num] == -1:
                flag = True
                if decision_arr == []:
                    ep_move_phase1[mse][idxes[mse]][twist_to_idx[twist]] = [n_idxes[mse]]
                else:
                    ep_move_phase1[mse][idxes[mse]][twist_to_idx[twist]][decision_num] = n_idxes[mse]
                #print(ep_move_phase1[mse][idxes[mse]][twist_to_idx[twist]])
        if flag:
            que.append(n_puzzle)
with open('move_table/move_ep_phase1.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for mse in ep_move_phase1:
        for all_status in mse:
            for twist in all_status:
                writer.writerow(twist)
