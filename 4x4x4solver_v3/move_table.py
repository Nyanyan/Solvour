from cube_class import Cube
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
with open('move_cp.csv', mode='w') as f:
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
with open('move_co.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in co_move:
        writer.writerow(arr)
'''

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
with open('move_ce_phase0.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for arr in ce_move_phase0:
        writer.writerow(arr)