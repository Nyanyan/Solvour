from cube_class import Cube, face, axis, wide, idx_ep_phase2, move_ep
from collections import deque, Counter
import csv
from time import time

def move_ce_phase0_func(puzzle, twist):
    return move_ce_phase0[puzzle][twist_to_idx[twist]]

def move_ce_phase1_func(puzzle, twist):
    return move_ce_phase1_fbud[puzzle // 70][twist_to_idx[twist]] * 70 + move_ce_phase1_rl[puzzle % 70][twist_to_idx[twist]]

def move_ce_phase2_func(puzzle, twist):
    return move_ce_phase2[puzzle][twist_to_idx[twist]]

def move_ep_phase1_func(puzzle_arr, twist):
    decision = [
        [[], [], [2, 3, 6, 7], [18, 19, 22, 23], [11, 10, 9, 8], [15, 14, 13, 12]], 
        [[12, 13, 10, 11], [8, 9, 14, 15], [0, 1, 4, 5], [16, 17, 20, 21], [], []],
        [[3, 2, 19, 18], [7, 6, 23, 22], [], [], [5, 4, 17, 16], [1, 0, 21, 20]]
        ]
    mse_lst = [[0, 0], [0, 1], [1, 2], [1, 3], [0, 2], [0, 3], [1, 0], [1, 1], [2, 1], [2, 0], [2, 3], [2, 2], [2, 5], [2, 4], [2, 7], [2, 6], [0, 4], [0, 5], [1, 4], [1, 5], [0, 6], [0, 7], [1, 6], [1, 7]]
    res = [-1, -1, -1]
    puzzle = [puzzle_arr // 65536, (puzzle_arr // 256) % 256, puzzle_arr % 256]
    for mse in range(3):
        decision_num = 0
        #print('decision', decision[mse][twist // 6])
        for i in decision[mse][twist // 6]:
            m_mse = mse_lst[i][0]
            shift = mse_lst[i][1]
            #print('shift', shift)
            decision_num *= 2
            #print(int((puzzle[m_mse] >> (7 - shift)) & 1 != i % 2))
            decision_num += int((puzzle[m_mse] >> (7 - shift)) & 1)
        #print('dec', decision_num)
        #print(move_ep_phase1[mse][puzzle[mse]][twist_to_idx[twist]])
        res[mse] = move_ep_phase1[mse][puzzle[mse]][twist_to_idx[twist]][decision_num]
    res = res[0] * 65536 + res[1] * 256 + res[2]
    return res

#                  0    1     2     3     4      5      6    7     8     9     10     11     12   13    14    15    16     17     18   19   20     21    22     23     24   25    26    27    28     29     30   31    32    33    34     35
move_candidate = ["R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "Lw", "Lw2", "Lw'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "Dw", "Dw2", "Dw'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'", "Bw", "Bw2", "Bw'"]
successor = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14, 15, 16, 17, 18, 19, 20,             24, 25, 26, 27, 28, 29, 30, 31, 32            ], # phase 0
            [0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            ], # phase 1
            [   1,       4,       7,               12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            ], # phase 2
            [   1,       4,       7,               12, 13, 14,             18, 19, 20,                 25,         28,         31,               ], # phase 3
            [0,    2,          6,    8,            12, 13, 14,             18, 19, 20,             24,     26,             30,     32            ], # phase 4
            [   1,                7,               12, 13, 14,             18, 19, 20,                 25,                     31                ]  # phase 5
            ]

twist_to_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, -1, -1, -1, 9, 10, 11, 12, 13, 14, 15, 16, 17, -1, -1, -1, 18, 19, 20, 21, 22, 23, 24, 25, 26, -1, -1, -1]

move_ce_phase0 = [[] for _ in range(735471)]
with open('move_table/move_ce_phase0.csv', mode='r') as f:
    for idx in range(735471):
        move_ce_phase0[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ce_phase1_fbud = [[] for _ in range(12870)]
with open('move_table/move_ce_phase1_fbud.csv', mode='r') as f:
    for idx in range(12870):
        move_ce_phase1_fbud[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ce_phase1_rl = [[] for _ in range(70)]
with open('move_table/move_ce_phase1_rl.csv', mode='r') as f:
    for idx in range(70):
        move_ce_phase1_rl[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ep_phase1 = [[[[] for _ in range(27)] for _ in range(256)] for _ in range(3)]
with open('move_table/move_ep_phase1.csv', mode='r') as f:
    for mse in range(3):
        for all_twist in range(256):
            for twist in range(27):
                move_ep_phase1[mse][all_twist][twist] = [int(i) for i in f.readline().replace('\n', '').split(',')]
move_ce_phase2 = [[] for _ in range(343000)]
with open('move_table/move_ce_phase2.csv', mode='r') as f:
    for idx in range(343000):
        move_ce_phase2[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]




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
        n_puzzle = move_ce_phase0_func(puzzle, twist)
        if prunning[n_puzzle] > num + 1:
            prunning[n_puzzle] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])
with open('prun_table/prunning0.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


#puzzle = Cube()
#print(puzzle.move(3).idx_ce_phase1_fbud() * 70 + puzzle.move(3).idx_ce_phase1_rl())
#print(move_ce_phase1_func(puzzle.idx_ce_phase1_fbud() * 70 + puzzle.idx_ce_phase1_rl(), 3))

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
        n_puzzle = move_ce_phase1_func(puzzle, twist)
        if n_puzzle // 70 == 0 and ce_parity[n_puzzle % 70] == 0:
            if prunning[n_puzzle] != 0:
                prunning[n_puzzle] = 0
                que.append([n_puzzle, 0, -10, -10, -10])
        elif prunning[n_puzzle] > num + 1:
            prunning[n_puzzle] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])

with open('prun_table/prunning1.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


# phase1 low & high edges
solved = Cube()
print('phase 1 2/2')
prunning = [99 for _ in range(8421504)]
solved_idx = solved.idx_high_low_edge()
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
        n_puzzle = move_ep_phase1_func(puzzle, twist)
        if prunning[n_puzzle // 2] > num + 1:
            prunning[n_puzzle // 2] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])

with open('prun_table/prunning1.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


# phase2 CE
print('phase 2 1/2')
iscolumn = [None for _ in range(343000)]
solved = Cube()
que = deque([solved])
while que:
    puzzle = que.popleft()
    for twist in successor[2]:
        n_puzzle = puzzle.move(twist)
        idx = n_puzzle.idx_ce_phase2()
        if iscolumn[idx] == None:
            iscolumn[idx] = n_puzzle.iscolumn()
            que.append(n_puzzle)
#print(iscolumn[:100])
prunning = [99 for _ in range(343000)]
solved_idx = solved.idx_ce_phase2()
prunning[solved_idx] = 0
que = deque([[solved_idx, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 10000 == 0:
        #tmp = prunning.count(100)
        print(cnt, len(que))
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    for twist in successor[2]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = move_ce_phase2_func(puzzle, twist)
        if iscolumn[n_puzzle]:
            if prunning[n_puzzle] != 0:
                prunning[n_puzzle] = 0
                que.append([n_puzzle, 0, -10, -10, -10])
        elif prunning[n_puzzle] > num + 1:
            prunning[n_puzzle] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])
with open('prun_table/prunning2.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


def edge_paired_4(ep):
    for i in range(4, 8):
        if ep[i * 2] // 2 != ep[i * 2 + 1] // 2:
            return False
    return True

# phase2 EP
print('phase 2 2/2')
solved = Cube()
prunning = [[99 for _ in range(665280)] for _ in range(2)]
solved_idx = idx_ep_phase2(solved.Ep)
prunning[0][solved_idx[0]] = 0
prunning[1][solved_idx[1]] = 0
que = deque([[solved.Ep, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 10000 == 0:
        print(cnt, len(que))
    puzzle, num, l1_twist, l2_twist, l3_twist = que.popleft()
    for twist in successor[2]:
        if face(twist) == face(l1_twist) or axis(twist) == axis(l1_twist) == axis(l2_twist) == axis(l3_twist) or (axis(twist) == axis(l1_twist) and wide(twist) == wide(l1_twist) == 1):
            continue
        n_puzzle = move_ep(puzzle, twist)
        idxes = idx_ep_phase2(n_puzzle)
        if edge_paired_4(n_puzzle):
            if prunning[0][idxes[0]] != 0 or prunning[1][idxes[1]] != 0:
                prunning[0][idxes[0]] = 0
                prunning[1][idxes[1]] = 0
                que.append([n_puzzle, 0, -10, -10, -10])
        elif prunning[0][idxes[0]] > num + 1 or prunning[1][idxes[1]] > num + 1:
            prunning[0][idxes[0]] = num + 1
            prunning[1][idxes[1]] = num + 1
            que.append([n_puzzle, num + 1, twist, l1_twist, l2_twist])
with open('prun_table/prunning2.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in prunning:
        writer.writerow(arr)

'''





















'''
# phase 0
solved = Cube()
print('phase 0 1/1')
prunning = [100 for _ in range(1471000)]
prunning[solved.phase_idx(0)] = 0
que = deque([[solved, 0, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 10000 == 0:
        #tmp = prunning.count(100)
        print(cnt, len(que))
        #print(prunning[0])
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[0]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        idx = n_status.phase_idx(0)
        if prunning[idx] == 100:
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])
with open('prunning0.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)
'''



'''
# phase1 center
solved = Cube()
print('phase 1 1/2')
prunning = [100 for _ in range(900970)]
prunning[solved.phase_idx(1)[0]] = 0
que = deque([[solved, 0, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 10000 == 0:
        #tmp = prunning.count(100)
        print(cnt, len(que))
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[1]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        idx = n_status.phase_idx(1)[0]
        #print(idx)
        if idx // 70 == 0 and (not n_status.ce_parity()):
            if prunning[idx] != 0:
                prunning[idx] = 0
                que.append([n_status, 0, -10, -10])
        elif prunning[idx] > num + 1:
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning1.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


# phase1 low & high edges
solved = Cube()
print('phase 1 2/2')
prunning = [100 for _ in range(8388608)]
prunning[solved.phase_idx(1)[1]] = 0
que = deque([[solved, 0, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 10000 == 0:
        #tmp = prunning.count(100)
        print(cnt, len(que))
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[1]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        idx = n_status.phase_idx(1)[1]
        if prunning[idx] > num + 1:
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning1.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)
'''




'''
# phase2 1 Ce
solved = Cube()
print('phase 2 1/2')
prunning = [100 for _ in range(343000)]
idx = solved.phase_idx(2)[0]
prunning[idx] = 0
que = deque([[solved, 0, -10, -10]])
cnt = 0
while que:
    strt = time()
    cnt += 1
    if cnt % 10000 == 0:
        #tmp = prunning.count(100)
        print(cnt, len(que))
    #print(prunning[:50])
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[2]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        idx = n_status.phase_idx(2)[0]
        if n_status.iscolumn():
            if prunning[idx] != 0:
                #print('a')
                prunning[idx] = 0
                que.append([n_status, 0, -10, -10])
        elif prunning[idx] > num + 1:
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning2.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)


# phase2 2 Ep
solved = Cube()
print('phase 2 2/2')
prunning = [[100 for _ in range(665280)] for _ in range(2)]
_, idx1, idx2 = solved.phase_idx(2)
prunning[0][idx1] = 0
prunning[1][idx2] = 0
que = deque([[solved, 0, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 10000 == 0:
        #tmp = [prunning[i].count(100) for i in range(len(prunning))]
        print(cnt, len(que))
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[2]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        _, idx1, idx2 = n_status.phase_idx(2)
        if n_status.edge_paired_4():
            if prunning[0][idx1] != 0 or prunning[1][idx2] != 0:
                prunning[0][idx1] = 0
                prunning[1][idx2] = 0
                que.append([n_status, 0, -10, -10])
        else:
            flag = False
            if prunning[0][idx1] > num + 1:
                prunning[0][idx1] = num + 1
                flag = True
            if prunning[1][idx2] > num + 1:
                prunning[1][idx2] = num + 1
                flag = True
            if flag:
                que.append([n_status, num + 1, twist, l_mov])

with open('prunning2.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    for i in range(2):
        writer.writerow(prunning[i])
'''





'''
# phase3 1 Ce
solved = Cube()
print('phase 3 1/2')
prunning = [100 for _ in range(343000)]
que = deque([[solved, 0, -10, -10]])
prunning[solved.phase_idx(3)[0]] = 0
cnt = 0
while que:
    strt = time()
    cnt += 1
    if cnt % 1000 == 0:
        tmp = prunning.count(100)
        print(cnt, tmp, len(que))
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[3]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        idx = n_status.phase_idx(3)[0]
        if prunning[idx] > num + 1:
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning3.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)
'''
'''
# phase3 2 Ep
solved = Cube()
print('phase 3 2/2')
prunning = [[100 for _ in range(40320)] for _ in range(2)]
que = deque([[solved, 0, -10, -10]])
prunning[0][solved.phase_idx(3)[1]] = 0
cnt = 0
while que:
    strt = time()
    cnt += 1
    if cnt % 1000 == 0:
        tmp = prunning.count(100)
        print(cnt, tmp, len(que))
        if tmp == 0:
            break
    #print(prunning[:50])
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[3]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        idx = n_status.phase_idx(3)[1]
        parity = n_status.pp_parity()
        if n_status.edge_paired_8() and parity == 0:
            if prunning[0][idx] != 0:
                prunning[0][idx] = 0
                que.append([n_status, 0, -10, -10])
        elif prunning[parity][idx] > num + 1:
            prunning[parity][idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning3.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    for i in range(2):
        writer.writerow(prunning[i])
'''



'''
# phase4 1 CO
solved = Cube()
print('phase 4 1/2')
prunning = [100 for _ in range(2187)]
que = deque([[solved, 0, -10, -10]])
prunning[solved.phase_idx(4)[0]] = 0
cnt = 0
while que:
    strt = time()
    cnt += 1
    if cnt % 1000 == 0:
        tmp = prunning.count(100)
        print(cnt, tmp, len(que))
        if tmp == 0:
            break
    #print(prunning[:50])
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[4]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        idx = n_status.phase_idx(4)[0]
        if prunning[idx] > num + 1:
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning4.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)

# phase4 2 EO
solved = Cube()
print('phase 4 2/2')
prunning = [100 for _ in range(531522)]
que = deque([[solved, 0, -10, -10]])
prunning[solved.phase_idx(4)[1]] = 0
cnt = 0
while que:
    strt = time()
    cnt += 1
    if cnt % 1000 == 0:
        tmp = prunning.count(100)
        print(cnt, tmp, len(que))
        if tmp == 0:
            break
    #print(prunning[:50])
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[4]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        idx = n_status.phase_idx(4)[1]
        if prunning[idx] > num + 1:
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning4.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)
'''


'''
# phase5 1 CP
solved = Cube()
print('phase 5 1/2')
prunning = [100 for _ in range(40320)]
que = deque([[solved, 0, -10, -10]])
prunning[solved.phase_idx(5)[0]] = 0
cnt = 0
while que:
    strt = time()
    cnt += 1
    if cnt % 1000 == 0:
        print(cnt, len(que))
    #print(prunning[:50])
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[5]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        idx = n_status.phase_idx(5)[0]
        if prunning[idx] > num + 1:
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning5.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)



# phase5 2 EP
solved = Cube()
print('phase 5 2/2')
prunning = [[100 for _ in range(665280)] for _ in range(2)]
que = deque([[solved, 0, -10, -10]])
prunning[0][solved.phase_idx(5)[1]] = 0
prunning[1][solved.phase_idx(5)[2]] = 0
cnt = 0
while que:
    strt = time()
    cnt += 1
    if cnt % 1000 == 0:
        #tmp = prunning.count(100)
        print(cnt, len(que))
    #print(prunning[:50])
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[5]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        _, idx1, idx2 = n_status.phase_idx(5)
        flag = False
        if prunning[0][idx1] > num + 1:
            prunning[0][idx1] = num + 1
            flag = True
        if prunning[1][idx2] > num + 1:
            prunning[1][idx2] = num + 1
            flag = True
        if flag:
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning5.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    for i in range(2):
        writer.writerow(prunning[i])
'''

