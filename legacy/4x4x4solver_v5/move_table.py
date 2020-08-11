from cube_class import Cube, face, axis, wide, move_cp, move_co, move_ep, move_ce, move_candidate, twist_to_idx, successor, idx_ep_phase1, ep_switch_parity, cmb
from collections import deque
import csv

move_arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24, 25, 26, 27, 28, 29, 30, 31, 32]

'''
solved = Cube()
ce_move_phase0 = [[-1 for _ in range(len(move_arr))] for _ in range(735471)]
que = deque([solved])
cnt = 0
print('CE move index phase0 RL')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_ce_phase0_rl()
    #print(idx)
    if ce_move_phase0[idx][0] == -1:
        for twist in move_arr:
            n_puzzle = puzzle.move(twist)
            n_idx = n_puzzle.idx_ce_phase0()
            ce_move_phase0[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move/ce_phase0_rl.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ce_move_phase0:
        writer.writerow(arr)
'''
solved = Cube()
ce_move_phase0 = [[-1 for _ in range(len(move_arr))] for _ in range(735471)]
que = deque([solved])
cnt = 0
print('CE move index phase0 FB')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_ce_phase0_fb()
    #print(idx)
    if ce_move_phase0[idx][0] == -1:
        for twist in move_arr:
            n_puzzle = puzzle.move(twist)
            n_idx = n_puzzle.idx_ce_phase0_fb()
            ce_move_phase0[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move/ce_phase0_fb.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ce_move_phase0:
        writer.writerow(arr)

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
with open('move/move_ce_phase1_fbud.csv', mode='w') as f:
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
with open('move/move_ce_phase1_rl.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ce_move_phase1_rl:
        writer.writerow(arr)


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
    idx = puzzle.idx_ce_phase23()
    for twist in successor[2]:
        n_puzzle = puzzle.move(twist)
        n_idx = n_puzzle.idx_ce_phase23()
        if ce_move_phase2[idx][twist_to_idx[twist]] == -1:
            ce_move_phase2[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move/ce_phase23.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ce_move_phase2:
        writer.writerow(arr)


ep_move_phase3 = [[-1 for _ in range(len(move_arr))] for _ in range(40320)]
solved = Cube()
que = deque([solved])
cnt = 0
print('EP move index phase2')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_ep_phase3()
    for twist in successor[3]:
        n_puzzle = puzzle.move(twist)
        n_idx = n_puzzle.idx_ep_phase3()
        if ep_move_phase3[idx][twist_to_idx[twist]] == -1:
            ep_move_phase3[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move/ep_phase3.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ep_move_phase3:
        writer.writerow(arr)



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
with open('move/cp.csv', mode='w') as f:
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
with open('move/co.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in co_move:
        writer.writerow(arr)



ep_move_phase4 = [[-1 for _ in range(len(move_arr))] for _ in range(495)]
solved = Cube()
que = deque([solved])
cnt = 0
print('EP move index phase4')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_ep_phase4()
    for twist in successor[4]:
        n_puzzle = puzzle.move(twist)
        n_idx = n_puzzle.idx_ep_phase4()
        if ep_move_phase4[idx][twist_to_idx[twist]] == -1:
            ep_move_phase4[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move/ep_phase4.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ep_move_phase4:
        writer.writerow(arr)


ep_move_phase5_ud = [[-1 for _ in range(len(move_arr))] for _ in range(40320)]
solved = Cube()
que = deque([solved])
cnt = 0
print('EP move index phase5 UD')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_ep_phase5_ud()
    for twist in successor[5]:
        n_puzzle = puzzle.move(twist)
        n_idx = n_puzzle.idx_ep_phase5_ud()
        if ep_move_phase5_ud[idx][twist_to_idx[twist]] == -1:
            ep_move_phase5_ud[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move/ep_phase5_ud.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ep_move_phase5_ud:
        writer.writerow(arr)


ep_move_phase5_fbrl = [[-1 for _ in range(len(move_arr))] for _ in range(24)]
solved = Cube()
que = deque([solved])
cnt = 0
print('EP move index phase5 FBRL')
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle = que.popleft()
    idx = puzzle.idx_ep_phase5_fbrl()
    for twist in successor[5]:
        n_puzzle = puzzle.move(twist)
        n_idx = n_puzzle.idx_ep_phase5_fbrl()
        if ep_move_phase5_fbrl[idx][twist_to_idx[twist]] == -1:
            ep_move_phase5_fbrl[idx][twist_to_idx[twist]] = n_idx
            que.append(n_puzzle)
with open('move/ep_phase5_fbrl.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ep_move_phase5_fbrl:
        writer.writerow(arr)
'''