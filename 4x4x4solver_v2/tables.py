from collections import deque, Counter
import csv
from time import time

class Cube:
    def __init__(self, cp=list(range(8)), co=[0 for _ in range(8)], ep=list(range(24)), ce=[i // 4 for i in range(24)]):
        self.Cp = cp
        self.Co = co
        self.Ep = ep
        self.Ce = ce
    
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
        pls = [2, 1, 2, 1]
        res = [i for i in self.Co]
        mov_type = mov // 6
        mov_amount = mov % 3
        for i in range(4):
            res[surface[mov_type][(i + mov_amount + 1) % 4]] = self.Co[surface[mov_type][i]]
            if mov_type // 2 != 1 and mov_amount != 1:
                res[surface[mov_type][(i + mov_amount + 1) % 4]] += pls[(i + mov_amount + 1) % 4]
                res[surface[mov_type][(i + mov_amount + 1) % 4]] %= 3
        return res
    
    def move_ep(self, mov):
        surface = [[[3, 12, 19, 10], [2, 13, 18, 11]], # R
                   [[3, 12, 19, 10], [2, 13, 18, 11], [4, 1, 20, 17]],  # Rw
                   [[7, 8, 23, 14], [6, 9, 22, 15]], # L
                   [[7, 8, 23, 14], [6, 9, 22, 15], [0, 5, 16, 21]], # Lw
                   [[0, 2, 4, 6], [1, 3, 5, 7]], # U
                   [[0, 2, 4, 6], [1, 3, 5, 7], [15, 12, 11, 8]], # Uw
                   [[16, 18, 20, 22], [17, 19, 21, 23]], # D
                   [[16, 18, 20, 22], [17, 19, 21, 23], [9, 10, 13, 14]], # Dw
                   [[5, 11, 17, 9], [4, 10, 16, 8]], # F
                   [[5, 11, 17, 9], [4, 10, 16, 8], [6, 3, 18, 23]], # Fw
                   [[1, 15, 21, 13], [0, 14, 20, 12]], # B
                   [[1, 15, 21, 13], [0, 14, 20, 12], [2, 7, 22, 19]] # Bw
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
        return Cube(cp=self.move_cp(mov), co=self.move_co(mov), ep=self.move_ep(mov), ce=self.move_ce(mov))

    def phase_idx(self, phase):
        res = 0
        rl_center = [8, 9, 10, 11, 16, 17, 18, 19]
        fb_center = [4, 5, 6, 7, 12, 13, 14, 15]
        ud_center = [0, 1, 2, 3, 20, 21, 22, 23]
        if phase == 0:
            cnt = 0
            for i in range(23):
                if self.Ce[i] == 2 or self.Ce[i] == 4:
                    res += cmb(23 - i, 8 - cnt)
                    cnt += 1
                    if cnt == 8 or i - cnt == 15:
                        break
            return res * 2 + self.ce_parity()
        elif phase == 1:
            cnt = 0
            arr = [0, 1, 2, 3, 20, 21, 22, 23, 4, 5, 6, 7, 12, 13, 14, 15] # FBUD centers
            for i in range(15):
                if self.Ce[arr[i]] == 1 or self.Ce[arr[i]] == 3:
                    res += cmb(15 - i, 8 - cnt)
                    cnt += 1
                    if cnt == 8 or i - cnt == 7:
                        break
            '''
            res2 = 0
            cnt = 0
            arr = [8, 9, 10, 11, 16, 17, 18, 19] # RL centers
            for i in range(8):
                if self.Ce[arr[i]] == 4:
                    res2 += cmb(7 - i, 4 - cnt)
                    cnt += 1
                    if cnt == 4 or i - cnt == 3:
                        break
            '''
            res3 = 0
            for i in range(23):
                res3 *= 2
                if self.Ep[i] % 2 != i % 2:
                    res3 += 1
            '''
            res4 = 0
            for i in range(12, 24):
                res4 *= 2
                if self.Ep[i] % 2 != i % 2:
                    res4 += 1
            '''
            return res, res3
        elif phase == 2:
            res0 = 0
            '''
            cnt = 0
            for i in range(7):
                if self.Ce[rl_center[i]] == 4:
                    res0 += cmb(7 - i, 4 - cnt)
                    cnt += 1
                    if cnt == 4 or i - cnt == 3:
                        break
            res0 *= 70
            '''
            cnt = 0
            for i in range(7):
                if self.Ce[fb_center[i]] == 3:
                    res0 += cmb(7 - i, 4 - cnt)
                    cnt += 1
                    if cnt == 4 or i - cnt == 3:
                        break
            res0 *= 70
            cnt = 0
            for i in range(7):
                if self.Ce[ud_center[i]] == 5:
                    res0 += cmb(7 - i, 4 - cnt)
                    cnt += 1
                    if cnt == 4 or i - cnt == 3:
                        break
            res1 = 0
            tmp = [4, 5, 6, 7]
            arr1 = [self.Ep[i] // 2 for i in range(1, 24, 2)]
            arr2 = [self.Ep[i] // 2 for i in range(0, 23, 2)]
            #print(arr1)
            #print(arr2)
            arr3 = [-1 for _ in range(12)]
            for i in range(12):
                arr3[i] = arr2.index(arr1[i])
            #print(arr3)
            res1 = 0
            for i in range(6):
                cnt = arr3[i]
                for j in arr3[:i]:
                    if j < arr3[i]:
                        cnt -= 1
                res1 += cnt * cmb(11 - i, 5 - i) * fac[5 - i]
            #print(res1)
            res2 = 0
            for i in range(6, 12):
                cnt = arr3[i]
                for j in arr3[6:i]:
                    if j < arr3[i]:
                        cnt -= 1
                res2 += cnt * cmb(11 - i + 6, 5 - i + 6) * fac[5 - i + 6]
            #print(res1, res2)
            #print('')
            return res0, res1, res2
        elif phase == 3:
            cnt = 0
            res0 = 0
            for i in range(7):
                if self.Ce[rl_center[i]] == 4:
                    res0 += cmb(7 - i, 4 - cnt)
                    cnt += 1
                    if cnt == 4 or i - cnt == 3:
                        break
            res0 *= 70
            cnt = 0
            for i in range(7):
                if self.Ce[fb_center[i]] == 3:
                    res0 += cmb(7 - i, 4 - cnt)
                    cnt += 1
                    if cnt == 4 or i - cnt == 3:
                        break
            res0 *= 70
            cnt = 0
            for i in range(7):
                if self.Ce[ud_center[i]] == 5:
                    res0 += cmb(7 - i, 4 - cnt)
                    cnt += 1
                    if cnt == 4 or i - cnt == 3:
                        break
            res1 = 0
            arr1 = [0, 2, 4, 6, 16, 18, 20, 22]
            arr1_p = [self.Ep[i] // 2 for i in arr1]
            arr2 = [1, 3, 5, 7, 17, 19, 21, 23]
            arr2_p = [self.Ep[i]// 2 for i in arr2]
            '''
            arr1_tmp = sorted(arr1_p)
            for i in range(8):
                arr1_p[i] = arr1_tmp.index(arr1_p[i])
            arr2_tmp = sorted(arr2_p)
            for i in range(8):
                arr2_p[i] = arr2_tmp.index(arr2_p[i])
            '''
            arr3 = [-1 for _ in range(8)]
            for i in range(8):
                arr3[i] = arr2_p.index(arr1_p[i])
            for i in range(7):
                cnt = arr3[i]
                for j in arr3[i + 1:]:
                    if j < arr3[i]:
                        cnt -= 1
                res1 += fac[7 - i] * (arr3[i] - cnt)
            return res0, res1
        elif phase == 4:
            res0 = 0
            for i in self.Co[:7]:
                res0 *= 3
                res0 += i
            res1 = 0
            for i in [0, 2, 4, 6, 16, 18, 20, 22]:
                res1 *= 3
                if self.Ep[i] // 2 in {0, 1, 2, 3, 8, 9, 10, 11}:
                    tmp = self.Ep[i] % 2
                    res1 += tmp
                else:
                    res1 += 2
            res2 = 0
            for i in [8, 10, 12, 14]:
                res2 *= 3
                if self.Ep[i] // 2 in {4, 5, 6, 7}:
                    tmp = self.Ep[i] % 2
                    res2 += tmp
                else:
                    res2 += 2
            return res0, res1 * 81 + res2
        elif phase == 5:
            res0 = 0
            for i in range(8):
                cnt = self.Cp[i]
                for j in self.Cp[:i]:
                    if j < self.Cp[i]:
                        cnt -= 1
                res0 += fac[7 - i] * cnt
            res1 = 0
            for i in range(6):
                cnt = self.Ep[i * 2] // 2
                for j in range(i):
                    if self.Ep[j * 2] < self.Ep[i * 2]:
                        cnt -= 1
                res1 += fac[5 - i] * cnt * cmb(11 - i, 5 - i)
            res2 = 0
            for i in range(6, 12):
                cnt = self.Ep[i * 2] // 2
                for j in range(6, i):
                    if self.Ep[j * 2] < self.Ep[i * 2]:
                        cnt -= 1
                res2 += fac[5 - i + 6] * cnt * cmb(11 - i + 6, 5 - i + 6)
            return res0, res1, res2
    
    def ce_parity(self):
        if (self.Ce[8] == self.Ce[11] and self.Ce[9] == self.Ce[10] and self.Ce[16] == self.Ce[19] and self.Ce[17] == self.Ce[18]) or (self.Ce[8] == self.Ce[9] and self.Ce[10] == self.Ce[11] and self.Ce[16] == self.Ce[17] and self.Ce[18] == self.Ce[19]) or (self.Ce[8] == self.Ce[10] == self.Ce[16] == self.Ce[18]):
            res2 = 0
        else:
            res2 = 1
        return res2
    
    def iscolumn(self):
        ng_arr = [[i, i + 2] for i in [0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21]]
        all_arr = [list(range(i, i + 4)) for i in range(0, 24, 4)]
        arr = [[4, 7], [5, 6], [8, 11], [9, 10], [12, 15], [13, 14], [16, 19], [17, 18]]
        for m_arr in arr:
            if self.Ce[m_arr[0]] != self.Ce[m_arr[1]]:
                return False
        return True
    
    def edge_paired_4(self):
        for i in range(4, 8):
            if self.Ep[i * 2] // 2 != self.Ep[i * 2 + 1] // 2:
                return False
        return True
    
    def edge_paired_8(self):
        for i in [0, 1, 2, 3, 8, 9, 10, 11]:
            if self.Ep[i * 2] // 2 != self.Ep[i * 2 + 1] // 2:
                return False
        return True
    
    def ep_parity(self):
        res = 0
        arr = [i for i in self.Ep]
        for i in range(24):
            if arr[i] != i:
                for j in range(i + 1, 24):
                    if arr[j] == i:
                        arr[i], arr[j] = arr[j], arr[i]
                        res += 1
        res %= 4
        return res
    
    def edge_separated(self):
        if set([self.Ep[i] // 2 for i in range(0, 24, 2)]) == set([self.Ep[i] // 2 for i in range(1, 24, 2)]):
            return True
        return False


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
            [0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14, 15, 16, 17, 18, 19, 20,             24, 25, 26, 27, 28, 29, 30, 31, 32            ], # phase 0
            [0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            ], # phase 1
            [   1,       4,       7,               12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            ], # phase 2
            [   1,       4,       7,               12, 13, 14,             18, 19, 20,                 25,         28,         31,               ], # phase 3
            [0,    2,          6,    8,            12, 13, 14,             18, 19, 20,             24,     26,             30,     32            ], # phase 4
            [   1,                7,               12, 13, 14,             18, 19, 20,                 25,                     31                ]  # phase 5
            ]




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
prunning = [100 for _ in range(12871)]
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
        if idx == 0: # and n_status.ce_parity() == 0:
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
prunning = [100 for _ in range(4900)]
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
# phase3 1 Ep
solved = Cube()
print('phase 3 2/2')
prunning = [100 for _ in range(40320)]
que = deque([[solved, 0, -10, -10]])
prunning[solved.phase_idx(3)[1]] = 0
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
        if n_status.edge_paired_8():
            if prunning[idx] != 0:
                prunning[idx] = 0
                que.append([n_status, 0, -10, -10])
        elif prunning[idx] > num + 1:
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning3.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)
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








