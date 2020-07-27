from cube_class import Cube, face, axis, wide, move_cp, move_co, move_ep, move_ce, move_candidate, twist_to_idx, successor, idx_ep_phase1, ep_switch_parity
from collections import deque
import csv

'''
move_ce_phase0 = [[] for _ in range(735471)]
with open('move/move_ce_phase0.csv', mode='r') as f:
    for idx in range(735471):
        move_ce_phase0[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ce_phase1_fbud = [[] for _ in range(12870)]
with open('move/move_ce_phase1_fbud.csv', mode='r') as f:
    for idx in range(12870):
        move_ce_phase1_fbud[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ce_phase1_rl = [[] for _ in range(70)]
with open('move/move_ce_phase1_rl.csv', mode='r') as f:
    for idx in range(70):
        move_ce_phase1_rl[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
'''
move_ep_phase1 = [[] for _ in range(2704156)]
with open('move/move_ep_phase1.csv', mode='r') as f:
    for idx in range(2704156):
        move_ep_phase1[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]

'''
# phase 0
solved = Cube()
print('phase 0 1/1')
prunning = [99 for _ in range(735471)]
solved_idx = solved.idx_ce_phase0()
prunning[solved_idx] = 0
que = deque([[solved_idx, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 10000 == 0:
        #tmp = prunning.count(100)
        print(cnt, len(que))
        #print(prunning[0])
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    for twist in successor[0]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = move_ce_phase0[puzzle][twist_to_idx[twist]]
        if prunning[n_puzzle] > num + 1:
            prunning[n_puzzle] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])
with open('prun/prunning0.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)

# phase1 center
ce_parity = [-1 for _ in range(70)]
solved = Cube()
que = deque([solved])
while que:
    puzzle = que.popleft()
    for twist in successor[1]:
        n_puzzle = puzzle.move(twist)
        idx = n_puzzle.idx_ce_phase1_rl()
        if ce_parity[idx] == -1:
            ce_parity[idx] = n_puzzle.ce_parity()
            que.append(n_puzzle)
print(ce_parity)
solved = Cube()
print('phase 1 1/2')
prunning = [99 for _ in range(900970)]
solved_idx = solved.idx_ce_phase1_fbud() * 70 + solved.idx_ce_phase1_rl()
prunning[solved_idx] = 0
que = deque([[solved_idx, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 10000 == 0:
        #tmp = prunning.count(100)
        print(cnt, len(que))
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    for twist in successor[1]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = move_ce_phase1_fbud[puzzle // 70][twist_to_idx[twist]] * 70 + move_ce_phase1_rl[puzzle % 70][twist_to_idx[twist]]
        if n_puzzle // 70 == 0 and ce_parity[n_puzzle % 70] == 0:
            if prunning[n_puzzle] != 0:
                prunning[n_puzzle] = 0
                que.append([n_puzzle, 0, -10, -10, -10])
        elif prunning[n_puzzle] > num + 1:
            prunning[n_puzzle] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])

with open('prun/prunning1.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


# phase1 ep
solved = Cube()
print('phase 1 2/2')
prunning = [99 for _ in range(2704156)]
solved_idx = idx_ep_phase1(solved.Ep)
prunning[solved_idx] = 0
que = deque([[solved_idx, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    if cnt % 10000 == 0:
        print(cnt, len(que), num)
    for twist in successor[1]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = move_ep_phase1[puzzle][twist_to_idx[twist]]
        if prunning[n_puzzle] > num + 1:
            prunning[n_puzzle] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])

with open('prun/prunning1.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)
'''