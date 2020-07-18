import tkinter
from collections import deque
import csv

class Cube:
    def __init__(self):
        self.Cp = [i for i in range(8)]
        self.Co = [0 for _ in range(8)]
        self.Ep = [i for i in range(24)]
        self.Ce = [i // 4 for i in range(24)]
    
    def move_cp(self, mov):
        surface = [[3, 1, 7, 5], [0, 2, 4, 6], [0, 1, 3, 2], [4, 5, 7, 6], [2, 3, 5, 4], [1, 0, 6, 7]]
        res = [i for i in self.Cp]
        mov_type = mov // 6
        mov_amount = mov % 3
        for i in range(4):
            res[surface[mov_type][(i + mov_amount + 1) % 4]] = self.Cp[surface[mov_type][i]]
        return res
    
    def move_co(self, mov):
        surface = [[3, 1, 7, 5], [0, 2, 4, 6], [0, 1, 3, 2], [4, 5, 7, 6], [2, 3, 5, 4], [1, 0, 6, 7]]
        pls = [1, 2, 1, 2]
        res = [i for i in self.Co]
        mov_type = mov // 6
        mov_amount = mov % 3
        for i in range(4):
            res[surface[mov_type][(i + mov_amount + 1) % 4]] = self.Co[surface[mov_type][i]]
            if mov // 9 != 1 and mov_amount != 1:
                res[surface[mov_type][(i + mov_amount + 1) % 4]] += pls[i]
                res[surface[mov_type][(i + mov_amount + 1) % 4]] %= 3
        return res
    
    def move_ep(self, mov):
        surface = [[[3, 12, 19, 11], [2, 13, 18, 10]], # R
                   [[3, 12, 19, 11], [2, 13, 18, 10], [4, 1, 20, 17]],  # Rw
                   [[7, 8, 23, 15], [6, 9, 22, 14]], # L
                   [[7, 8, 23, 15], [6, 9, 22, 14], [0, 5, 16, 21]], # Lw
                   [[0, 2, 4, 6], [1, 3, 5, 7]], # U
                   [[0, 2, 4, 6], [1, 3, 5, 7], [14, 12, 10, 8]], # Uw
                   [[16, 18, 20, 22], [17, 19, 21, 23]], # D
                   [[16, 18, 20, 22], [17, 19, 21, 23], [9, 11, 13, 15]], # Dw
                   [[5, 10, 17, 9], [4, 11, 16, 8]], # F
                   [[5, 10, 17, 9], [4, 11, 16, 8], [6, 3, 18, 23]], # Fw
                   [[1, 14, 21, 13], [0, 15, 20, 12]], # B
                   [[1, 14, 21, 13], [0, 15, 20, 12], [2, 7, 22, 19]] # Bw
                   ]
        mov_type = mov // 3
        mov_amount = mov % 3
        res = [i for i in self.Ep]
        for arr in surface[mov_type]:
            for i in range(4):
                res[arr[(i + mov_amount + 1) % 4]] = self.Ep[arr[i]]
        return res
    
    def move_ce(self, mov):
        surface = [[[8, 9, 10, 11]], # R
                   [[8, 9, 10, 11], [2, 12, 22, 6], [1, 15, 21, 5]], # Rw
                   [[16, 17, 18, 19]], # L
                   [[16, 17, 18, 19], [0, 4, 20, 14], [3, 7, 23, 13]], # Lw
                   [[0, 1, 2, 3]], # U
                   [[0, 1, 2, 3], [13, 9, 5, 17], [12, 8, 4, 16]], # Uw
                   [[20, 21, 22, 23]], # D
                   [[20, 21, 22, 23], [7, 11, 15, 19], [6, 10, 14, 18]], # Dw
                   [[4, 5, 6, 7]], # F
                   [[4, 5, 6, 7], [3, 8, 21, 18], [2, 11, 20, 17]], # Fw
                   [[12, 13, 14, 15]], # B
                   [[12, 13, 14, 15], [1, 16, 23, 10], [0, 19, 22, 9]] # Bw
                   ]
        mov_type = mov // 3
        mov_amount = mov % 3
        res = [i for i in self.Ce]
        for arr in surface[mov_type]:
            for i in range(4):
                res[arr[(i + mov_amount + 1) % 4]] = self.Ce[arr[i]]
        return res
    
    def move(self, mov):
        res = Cube()
        res.Cp = self.move_cp(mov)
        res.Co = self.move_co(mov)
        res.Ep = self.move_ep(mov)
        res.Ce = self.move_ce(mov)
        return res
    '''
    def idx(self): # Epの組み合わせが6e23くらいあるのでこれで枝刈りするのは無理
        res_cp = 0
        for i in range(8):
            cnt = 0
            for j in self.Cp[:i]:
                if j < self.Cp[i]:
                    cnt += 1
            res_cp += fac[7 - i] * (self.Cp[i] - cnt)
        res_co = 0
        for i in range(8):
            res_co *= 3
            res_co += self.Co[i]
        return res_cp, res_co
    '''
    def parity(self):
        res1 = 0
        for i in range(12):
            res1 *= 2
            if self.Ep[i] % 2 != i % 2:
                res1 += 1
        res2 = 0
        for i in range(12, 24):
            res2 *= 2
            if self.Ep[i] % 2 != i % 2:
                res2 += 1
        return res1, res2
    
    def sgn_ep(self):
        res = 0
        arr = [i for i in self.Ep]
        for i in range(24):
            if arr[i] != i:
                for j in range(i + 1, 24):
                    if arr[j] == i:
                        arr[i], arr[j] = arr[j], arr[i]
                        res += 1
        return res % 2
    
    def phase0_idx(self):
        res = 0
        cnt = 0
        for i in reversed(range(24)):
            if self.Ce[i] == 2 or self.Ce[i] == 4:
                cnt += 1
                res += cmb(23 - i, cnt)
        return res
    
    def phase1_idx(self):
        res = 0
        cnt = 0
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23]
        for i in reversed(range(16)):
            if self.Ce[arr[i]] == 1 or self.Ce[arr[i]] == 3:
                cnt += 1
                res += cmb(15 - i, cnt)
        return res
    
    def ce_phase2_idx(self):
        res_rl = 0
        cnt = 0
        for i in reversed(range(8)):
            if self.Ce[rl_center[i]] == 4:
                cnt += 1
                res_rl += cmb(7 - i, cnt)
        res_fb = 0
        cnt = 0
        for i in reversed(range(8)):
            if self.Ce[fb_center[i]] == 3:
                cnt += 1
                res_fb += cmb(7 - i, cnt)
        res_ud = 0
        cnt = 0
        for i in reversed(range(8)):
            if self.Ce[ud_center[i]] == 5:
                cnt += 1
                res_ud += cmb(7 - i, cnt)
        return res_rl * 4900 + res_fb * 70 + res_ud

    def phase_idx(self, phase):
        res = 0
        if phase == 0:
            cnt = 0
            for i in reversed(range(24)):
                if self.Ce[i] == 2 or self.Ce[i] == 4:
                    cnt += 1
                    res += cmb(23 - i, cnt)
        elif phase == 1:
            cnt = 0
            arr = [0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23]
            for i in reversed(range(16)):
                if self.Ce[arr[i]] == 1 or self.Ce[arr[i]] == 3:
                    cnt += 1
                    res += cmb(15 - i, cnt)
        return res

def cmb(n, r):
    return fac[n] // fac[r] // fac[n - r]

fac = [1 for _ in range(25)]
for i in range(1, 25):
    fac[i] = fac[i - 1] * i

solution = []
path = []
#                  0    1     2     3     4      5      6    7     8     9     10     11     12   13    14    15    16     17     18   19   20     21    22     23     24   25    26    27    28     29     30   31    32    33    34     35
move_candidate = ["R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "Lw", "Lw2", "Lw'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "Dw", "Dw2", "Dw'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'", "Bw", "Bw2", "Bw'"]
successor = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35], # phase 0
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,     16,     18, 19, 20,     22,     24, 25, 26,     28,     30, 31, 32,     34    ], # phase 1
            ]
solved = Cube()

prunning_num = [735471, 12870]

for phase in range(1, 2):
    prunning = [100 for _ in range(prunning_num[phase])]
    prunning[solved.phase_idx(phase)] = 0
    que = deque([[solved, 0, -10, -10]])
    cnt = 0
    while que:
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt)
        status, num, l_mov, l2_mov = que.popleft()
        l_twist_0 = l_mov // 3
        l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
        l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
        for twist in successor[phase]:
            if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
                continue
            n_status = status.move(twist)
            idx = n_status.phase_idx(phase)
            if prunning[idx] < 100:
                continue
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])
    
    with open('prunning' + str(phase) + '.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(prunning)


'''
ce_phase1 = [1000 for _ in range(735471)]
ce_phase1[solved.ce_phase1_idx()] = 0
que = deque([[solved, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 1000 == 0:
        print(cnt)
    #print(len(que))
    status, num, l_mov, l2_mov, l3_mov = que.popleft()
    l_mov_type = l_mov // 3
    l3_mov_type = l_mov // 9 if l_mov // 9 == l2_mov // 9 == l3_mov // 9 else -10
    lst = [0, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 20, 21, 23, 24, 26]
    for mov in lst:
        if l_mov_type == mov // 3 or l3_mov_type == mov // 9:
            continue
        n_status = status.move(mov)
        idx = n_status.ce_phase1_idx()
        if ce_phase1[idx] < 1000:
            continue
        ce_phase1[idx] = num + 1
        que.append([n_status, num + 1, mov, l_mov, l2_mov])

with open('ce_phase1.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(ce_phase1)
'''


'''
ce_phase2 = [1000 for _ in range(12870)]
ce_phase2[solved.ce_phase2_idx()] = 0
que = deque([[solved, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 1000 == 0:
        print(cnt)
    #print(len(que))
    status, num, l_mov, l2_mov, l3_mov = que.popleft()
    l_mov_type = l_mov // 3
    l3_mov_type = l_mov // 9 if l_mov // 9 == l2_mov // 9 == l3_mov // 9 else -10
    lst = [0, 2, 3, 5, 6, 8, 9, 11, 13, 15, 17, 18, 20, 22, 24, 26]
    for mov in lst:
        if l_mov_type == mov // 3 or l3_mov_type == mov // 9:
            continue
        n_status = status.move(mov)
        idx = n_status.ce_phase2_idx()
        if ce_phase2[idx] < 1000:
            continue
        ce_phase2[idx] = num + 1
        que.append([n_status, num + 1, mov, l_mov, l2_mov])

with open('ce_phase2.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(ce_phase2)
'''
'''
parity_phase2_1 = [1000 for _ in range(4096)]
parity_phase2_2 = [1000 for _ in range(4096)]
parity_idx = solved.parity()
parity_phase2_1[parity_idx[0]] = 0
parity_phase2_2[parity_idx[1]] = 0
que = deque([[solved, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 1000 == 0:
        print(cnt)
    #print(len(que))
    status, num, l_mov, l2_mov, l3_mov = que.popleft()
    l_mov_type = l_mov // 3
    l3_mov_type = l_mov // 9 if l_mov // 9 == l2_mov // 9 == l3_mov // 9 else -10
    lst = [0, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 20, 21, 23, 24, 26]
    for mov in lst:
        if l_mov_type == mov // 3 or l3_mov_type == mov // 9:
            continue
        n_status = status.move(mov)
        idx = n_status.parity()
        if parity_phase2_1[idx[0]] < 1000 and parity_phase2_2[idx[1]] < 1000:
            continue
        parity_phase2_1[idx[0]] = min(parity_phase2_1[idx[0]], num + 1)
        parity_phase2_2[idx[1]] = min(parity_phase2_2[idx[1]], num + 1)
        que.append([n_status, num + 1, mov, l_mov, l2_mov])

with open('parity_phase2_1.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(parity_phase2_1)
with open('parity_phase2_2.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(parity_phase2_2)
'''

'''
ce_phase3 = [1000 for _ in range(347970)]
ce_phase3[solved.ce_phase3_idx()] = 0

que = deque([[solved, 0, -10, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 1000 == 0:
        print(cnt)
    #print(len(que))
    status, num, l_mov, l2_mov, l3_mov = que.popleft()
    l_mov_type = l_mov // 3
    l3_mov_type = l_mov // 9 if l_mov // 9 == l2_mov // 9 == l3_mov // 9 else -10
    lst = [0, 2, 4, 6, 8, 9, 11, 13, 15, 17, 18, 20, 22, 24, 26]
    for mov in lst:
        if l_mov_type == mov // 3 or l3_mov_type == mov // 9:
            continue
        n_status = status.move(mov)
        idx = n_status.ce_phase3_idx()
        if ce_phase3[idx] < 1000:
            continue
        ce_phase3[idx] = num + 1
        que.append([n_status, num + 1, mov, l_mov, l2_mov])

with open('ce_phase3.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(ce_phase3)
'''