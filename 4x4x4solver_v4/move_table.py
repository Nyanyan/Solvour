from cube_class import Cube, face, axis, wide, move_cp, move_co, move_ep, move_ce, move_candidate, twist_to_idx, successor, idx_ep_phase1, ep_switch_parity, cmb
from collections import deque
import csv

move_arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24, 25, 26, 27, 28, 29, 30, 31, 32]

'''
solved = Cube()
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

solved = Cube()
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

solved = Cube()
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
'''
'''
solved = Cube()
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
        for twist in successor[1]:
            n_puzzle = puzzle.move(twist)
            n_idx = n_puzzle.idx_ce_phase1_fbud()
            ce_move_phase1_fbud[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move_table/move_ce_phase1_fbud.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ce_move_phase1_fbud:
        writer.writerow(arr)

solved = Cube()
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
        for twist in successor[1]:
            n_puzzle = puzzle.move(twist)
            n_idx = n_puzzle.idx_ce_phase1_rl()
            ce_move_phase1_rl[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move_table/move_ce_phase1_rl.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ce_move_phase1_rl:
        writer.writerow(arr)
'''
'''
def idx_to_ep_phase1(idx):
    res = [-1 for _ in range(24)]
    remain_1 = 12
    strt = 24
    for i in range(24):
        if idx == 0:
            strt = i
            break
        tmp = cmb(23 - i, remain_1)
        #print(i, 23 - i, remain_1, tmp, idx)
        res[i] = 1 if idx // tmp else 0
        idx -= tmp * res[i]
        if res[i] == 1:
            remain_1 -= 1
    for i in reversed(range(strt, 24)):
        if remain_1:
            res[i] = 1
            remain_1 -= 1
        else:
            res[i] = 0
    return res

ep_move_phase1 = [[-1 for _ in range(len(move_arr))] for _ in range(10000)]
for idx in range(2704156):
    arr_idx = idx % 10000
    ep = idx_to_ep_phase1(idx)
    for twist in successor[1]:
        n_ep = move_ep(ep, twist)
        n_idx = idx_ep_phase1(n_ep)
        ep_move_phase1[arr_idx][twist_to_idx[twist]] = n_idx
    if idx % 10000 == 9999:
        print(idx, idx / 2704156)
        with open('move/move_ep_phase1.csv', mode='a') as f:
            writer = csv.writer(f, lineterminator='\n')
            for arr in ep_move_phase1:
                writer.writerow(arr)
        ep_move_phase1 = [[-1 for _ in range(len(move_arr))] for _ in range(10000)]
with open('move/ep_phase1.csv', mode='a') as f:
        writer = csv.writer(f, lineterminator='\n')
        for arr in ep_move_phase1[:4156]:
            writer.writerow(arr)
'''

ce_move_phase2 = [[-1 for _ in range(len(move_arr))] for _ in range(343000)]
solved = Cube()
que = deque([solved])
cnt = 0
print('CE move index phase2')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_ce_phase2()
    for twist in successor[2]:
        n_puzzle = puzzle.move(twist)
        n_idx = n_puzzle.idx_ce_phase2()
        if ce_move_phase2[idx][twist_to_idx[twist]] == -1:
            ce_move_phase2[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move/ce_phase2.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ce_move_phase2:
        writer.writerow(arr)

''' 使っていない I don't use these
ep_move_phase2 = [[-1 for _ in range(len(move_arr))] for _ in range(343000)]
solved = Cube()
que = deque([solved])
cnt = 0
print('CE move index phase2')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_ce_phase2()
    for twist in successor[2]:
        n_puzzle = puzzle.move(twist)
        n_idx = n_puzzle.idx_ce_phase2()
        if ce_move_phase2[idx][twist_to_idx[twist]] == -1:
            ce_move_phase2[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move/ce_phase2.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ce_move_phase2:
        writer.writerow(arr)
'''