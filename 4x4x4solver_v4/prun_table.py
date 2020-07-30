from cube_class import Cube, face, axis, wide, move_cp, move_co, move_ep, move_ce, move_candidate, twist_to_idx, successor, idx_ep_phase1, ep_switch_parity, idx_ep_phase2
from collections import deque
import csv


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


# phase2 ce
solved = Cube()
print('phase 2 1/2')
prunning = [99 for _ in range(343000)]
solved_idx = solved.idx_ce_phase23()
prunning[solved_idx] = 0
que = deque([[solved, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    if cnt % 10000 == 0:
        print(cnt, len(que))
    for twist in successor[2]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = puzzle.move(twist)
        n_idx = n_puzzle.idx_ce_phase23()
        if n_puzzle.iscolumn():
            if prunning[n_idx] > 0:
                prunning[n_idx] = 0
                que.append([n_puzzle, 0, -10, -10, -10])
        else:
            if prunning[n_idx] > num + 1:
                prunning[n_idx] = num + 1
                que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])

with open('prun/prunning2.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


# phase2 ep
solved = Cube()
print('phase 2 2/2')
prunning = [[99 for _ in range(665280)] for _ in range(2)]
solved_idx = idx_ep_phase2(solved.Ep)
for i in range(2):
    prunning[i][solved_idx[i]] = 0
que = deque([[solved, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    if cnt % 10000 == 0:
        print(cnt, len(que))
    for twist in successor[2]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = puzzle.move(twist)
        n_idx = idx_ep_phase2(n_puzzle.Ep)
        flag = False
        if n_puzzle.edge_paired_4():
            for i in range(2):
                if prunning[i][n_idx[i]] > 0:
                    prunning[i][n_idx[i]] = 0
                    flag = True
            if flag:
                que.append([n_puzzle, 0, -10, -10, -10])
        else:
            for i in range(2):
                if prunning[i][n_idx[i]] > num + 1:
                    prunning[i][n_idx[i]] = num + 1
                    flag = True
            if flag:
                que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])

with open('prun/prunning2.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in prunning:
        writer.writerow(arr)


# phase3 ce
solved = Cube()
print('phase 3 1/2')
prunning = [99 for _ in range(343000)]
solved_idx = solved.idx_ce_phase23()
prunning[solved_idx] = 0
que = deque([[solved_idx, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    if cnt % 10000 == 0:
        print(cnt, len(que))
    for twist in successor[3]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = move_ce_phase23[puzzle][twist_to_idx[twist]]
        if prunning[n_puzzle] > num + 1:
            prunning[n_puzzle] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])

with open('prun/prunning3.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


# phase3 ep
solved = Cube()
print('phase 3 2/2')
prunning = [99 for _ in range(40320)]
solved_idx = solved.idx_ep_phase3()
prunning[solved_idx] = 0
que = deque([[solved_idx, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    if cnt % 10000 == 0:
        print(cnt, len(que))
    for twist in successor[3]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = move_ep_phase3[puzzle][twist_to_idx[twist]]
        if prunning[n_puzzle] > num + 1:
            prunning[n_puzzle] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])

with open('prun/prunning3.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


# phase4 co
solved = Cube()
print('phase 4 1/2')
prunning = [99 for _ in range(2187)]
solved_idx = solved.idx_co()
prunning[solved_idx] = 0
que = deque([[solved_idx, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    if cnt % 10000 == 0:
        print(cnt, len(que))
    for twist in successor[4]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = move_co_arr[puzzle][twist_to_idx[twist]]
        if prunning[n_puzzle] > num + 1:
            prunning[n_puzzle] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])
with open('prun/prunning4.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


# phase4 ep
solved = Cube()
print('phase 4 2/2')
prunning = [99 for _ in range(495)]
solved_idx = solved.idx_ep_phase4()
prunning[solved_idx] = 0
que = deque([[solved_idx, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    if cnt % 10000 == 0:
        print(cnt, len(que))
    for twist in successor[4]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = move_ep_phase4[puzzle][twist_to_idx[twist]]
        if prunning[n_puzzle] > num + 1:
            prunning[n_puzzle] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])
with open('prun/prunning4.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


# phase5 cp
solved = Cube()
print('phase 5 1/2')
prunning = [99 for _ in range(40320)]
solved_idx = solved.idx_cp()
prunning[solved_idx] = 0
que = deque([[solved_idx, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    if cnt % 10000 == 0:
        print(cnt, len(que))
    for twist in successor[5]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = move_cp_arr[puzzle][twist_to_idx[twist]]
        if prunning[n_puzzle] > num + 1:
            prunning[n_puzzle] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])
with open('prun/prunning5.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


# phase5 ep
solved = Cube()
print('phase 5 1/2')
prunning = [99 for _ in range(967704)]
solved_idx = solved.idx_ep_phase5()
prunning[solved_idx] = 0
que = deque([[solved_idx, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    if cnt % 10000 == 0:
        print(cnt, len(que))
    for twist in successor[5]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = move_ep_phase5_ud[puzzle // 24][twist_to_idx[twist]] * 24 + move_ep_phase5_fbrl[puzzle % 24][twist_to_idx[twist]]
        if prunning[n_puzzle] > num + 1:
            prunning[n_puzzle] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])
with open('prun/prunning5.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)
