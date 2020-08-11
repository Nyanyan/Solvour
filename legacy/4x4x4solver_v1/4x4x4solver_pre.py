from collections import deque, Counter
import csv
from time import time

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
    '''
    '''
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
    '''
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
            return res
        elif phase == 1:
            cnt = 0
            arr = [0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23] # FBUDセンター
            for i in range(15):
                if self.Ce[arr[i]] == 1 or self.Ce[arr[i]] == 3:
                    res += cmb(15 - i, 8 - cnt)
                    cnt += 1
                    if cnt == 8 or i - cnt == 7:
                        break
            res2 = 0
            cnt = 0
            arr = [8, 9, 10, 11, 16, 17, 18, 19] # RLセンター
            for i in range(8):
                if self.Ce[arr[i]] == 2:
                    res2 += cmb(7 - i, 4 - cnt)
                    cnt += 1
                    if cnt == 4 or i - cnt == 3:
                        break
            res3 = 0
            for i in range(23):
                res3 *= 2
                if self.Ep[i] % 2 != i % 2:
                    res3 += 1
            return res, res2, res3
        elif phase == 2:
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
            '''
            arr4 = [i[0] for i in arr3]
            arr5 = [i[1] for i in arr3]
            #print(arr4)
            #print(arr5)
            arr4_marked = -1
            for i in range(3):
                for j in range(arr4_marked + 1, arr4[i]):
                    res1 += cmb(11 - j, 3 - i)
                arr4_marked = arr4[i]
            #print(res1)
            res1 *= 495
            for i in range(4):
                res1 += arr5[i] * cmb(11 - i, 3 - i)
            #print(res1)
            '''
            '''
            cnt = 0
            for i in range(11):
                if arr1[i] != 0:
                    res1 += cmb(11 - i, 4 - cnt)
                    cnt += 1
                    if cnt == 4 or i - cnt == 7:
                        break
            res1 *= 495
            cnt = 0
            for i in range(11):
                if arr2[i] == 1:
                    res1 += cmb(11 - i, 4 - cnt)
                    cnt += 1
                    if cnt == 4 or i - cnt == 7:
                        break
            '''
            '''
            if res1 >= 8217:
                print('res1', res1)
            if res2 >= 8217:
                print('res2', res2)
            '''
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
            arr1_p = [self.Ep[i] for i in arr1]
            arr2 = [1, 3, 5, 7, 17, 19, 21, 23]
            arr2_p = [self.Ep[i] for i in arr2]
            arr1_tmp = sorted(arr1_p)
            for i in range(8):
                arr1_p[i] = arr1_tmp.index(arr1_p[i])
            arr2_tmp = sorted(arr2_p)
            for i in range(8):
                arr2_p[i] = arr2_tmp.index(arr2_p[i])
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
    '''
    arr = []
    for i in [4, 5, 6, 7]:
        tmp2 = []
        for j in range(24):
            if tmp[j] == i:
                tmp2.append(j)
        if tmp2[0] % 2:
            tmp2[0], tmp2[1] = tmp2[1], tmp2[0]
        arr.append(tmp2)
    arr1 = [i[0] for i in arr]
    arr2 = [i[1] for i in arr]
    #print(arr)
    #arr.sort()
    #print(arr)
    arr2 = [arr[i][1] // 2 for i in range(4)]
    #print(arr2)
    for i in arr2:
        res1 *= 12
        res1 += i
    #print(res1)
    '''
    '''
    cnt = 0
    res0 = 0
    for i in reversed(range(8)):
        if self.Ce[rl_center[i]] == 4:
            cnt += 1
            res0 += cmb(7 - i, cnt)
    res0 *= 70
    cnt = 0
    for i in reversed(range(8)):
        if self.Ce[fb_center[i]] == 3:
            cnt += 1
            res0 += cmb(7 - i, cnt)
    res0 *= 70
    cnt = 0
    for i in reversed(range(8)):
        if self.Ce[ud_center[i]] == 5:
            cnt += 1
            res0 += cmb(7 - i, cnt)
    res1 = 0
    tmp = [i // 2 for i in self.Ep]
    arr = []
    for i in [0, 1, 2, 3, 8, 9, 10, 11]:
        tmp2 = []
        for j in range(24):
            if tmp[j] == i:
                tmp2.append(j)
        if tmp2[0] % 2:
            tmp2[0], tmp2[1] = tmp2[1], tmp2[0]
        arr.append(tmp2)
    #print(arr)
    arr.sort()
    #print(arr)
    arr2 = [arr[i][1] // 2 for i in range(8)]
    for i in range(8):
        if arr2[i] > 3:
            arr2[i] -= 4
    #print(arr2)
    for i in range(8):
        cnt = arr2[i]
        for j in arr2[i + 1:]:
            if j < arr2[i]:
                cnt -= 1
        res1 += fac[7 - i] * (arr2[i] - cnt)
    return res0, res1
    '''
    '''
    arr2 = [arr[i][1] // 2 for i in range(12)]
    for i in range(12):
        cnt = arr2[i]
        for j in arr2[i + 1:]:
            if j < arr2[i]:
                cnt -= 1
        res1 += fac[11 - i] * (arr2[i] - cnt)
    '''
    #print(res1)
    '''
    arr2 = [arr[i][1] // 2 for i in [4, 5, 6, 7]]
    #print(arr2)
    for i in arr2:
        res1 *= 12
        res1 += i
    #print(res1)
    '''
    '''
    res1 = [0, 0, 0]
    for ii in range(3):
        for i in range(8 * ii, 8 * (ii + 1)):
            cnt = self.Ep[i]
            for j in self.Ep[i + 1:8 * (ii + 1)]:
                if j < self.Ep[i]:
                    cnt -= 1
            res1[ii] += fac[7 - i + 8 * ii] * (self.Ep[i] - cnt)
    res = [res0]
    res.extend(res1)
    return res
    '''
    '''
    res1 = 0
    tmp = [self.Ep[i] // 2 for i in [8, 9, 10, 11, 12, 13, 14, 15]]
    #print(tmp)
    cntr = Counter(tmp)
    arr = [0 for _ in range(8)]
    idx = 1
    for i in range(8):
        if cntr[tmp[i]] == 2 and arr[i] == 0:
            for j in range(i, 8):
                if tmp[i] == tmp[j]:
                    arr[j] = idx
            idx += 1
    #print(arr)
    pair = max(arr)
    #print(pair)
    remain = [2 for _ in range(pair + 1)]
    remain[0] = 8 - 2 * pair
    #print(remain)
    strt = [0, 300, 600, 900, 1200]
    res2 = strt[pair]
    for i in range(8):
        for j in range(arr[i]): # その場所にもしjがあったら
            if remain[j] == 0:
                continue
            tmp2 = 7 - i
            for k in range(pair + 1): # その下のパーツの入り方
                #print('tmp2', tmp2)
                tmp = remain[k] - 1 if j == k else remain[k]
                if tmp == 0:
                    continue
                res2 += cmb(tmp2, tmp)
                tmp2 -= tmp
        remain[arr[i]] -= 1
        #print(remain, res2)
    return res2
    '''
    #return res
    def sgn(self):
        '''
        res = 0
        arr = [i for i in self.Ep]
        for i in range(24):
            if arr[i] != i:
                for j in range(i + 1, 24):
                    if arr[j] == i:
                        arr[i], arr[j] = arr[j], arr[i]
                        res += 1
        res %= 2
        '''
        if (self.Ce[8] == self.Ce[11] and self.Ce[16] == self.Ce[19]) or (self.Ce[8] == self.Ce[9] and self.Ce[16] == self.Ce[17]) or (self.Ce[8] == self.Ce[10] == self.Ce[16] == self.Ce[18]):
            res2 = 0
        else:
            res2 = 1
        return res2
    
    def iscolumn(self):
        ng_arr = [[i, i + 2] for i in [0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21]]
        all_arr = [list(range(i, i + 4)) for i in range(0, 24, 4)]
        arr = [[4, 7], [5, 6], [8, 11], [9, 10], [12, 15], [13, 14], [16, 19], [17, 18]]
        return_val = True
        for m_arr in arr:
            if self.Ce[m_arr[0]] != self.Ce[m_arr[1]]:
                return_val = False
                break
        return return_val
        '''
        for i in range(12):
            if self.Ce[ng_arr[i][0]] == self.Ce[ng_arr[i][1]]:
                if len(set([self.Ce[i] for i in all_arr[i // 2]])) != 1:
                    return False
        return True
        '''
    
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
    
    def sgn_mod4(self):
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


def cmb(n, r):
    return fac[n] // fac[r] // fac[n - r]

fac = [1 for _ in range(25)]
for i in range(1, 25):
    fac[i] = fac[i - 1] * i

solution = []
path = []
#                  0    1     2     3     4      5      6    7     8     9     10     11     12   13    14    15    16     17     18   19   20     21    22     23     24   25    26    27    28     29     30   31    32    33    34     35
move_candidate = ["R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "Lw", "Lw2", "Lw'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "Dw", "Dw2", "Dw'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'", "Bw", "Bw2", "Bw'"]
'''
successor = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35], # phase 0
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,     16,     18, 19, 20,     22,     24, 25, 26,     28,     30, 31, 32,     34    ], # phase 1
            [   1,       4,       7,       10,     12, 13, 14,     16,     18, 19, 20,     22,     24, 25, 26,     28,     30, 31, 32,     34    ], # phase 2
            [   1,       4,       7,       10,     12, 13, 14,             18, 19, 20,                 25,         28,         31,         34    ], # phase 3
            ]
'''
successor = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14, 15, 16, 17, 18, 19, 20,             24, 25, 26, 27, 28, 29, 30, 31, 32            ], # phase 0
            [0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32,           ], # phase 1
            [   1,       4,       7,               12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32,           ], # phase 2
            [   1,       4,       7,               12, 13, 14,             18, 19, 20,                 25,         28,         31,               ], # phase 3
            ]
solved = Cube()




'''
# phase 0
prunning_num = [735471, 12870]
for phase in range(1, 2):
    if phase == 1:
        prunning = [[100 for _ in range(prunning_num[phase])] for _ in range(4)]
        prunning[0][solved.phase_idx(phase)] = 0
    else:
        prunning = [100 for _ in range(prunning_num[phase])]
        prunning[solved.phase_idx(phase)] = 0
    
    que = deque([[solved, 0, -10, -10]])
    cnt = 0
    while que:
        cnt += 1
        if cnt % 1000 == 0:
            if phase == 0:
                tmp = prunning.count(100)
                print(cnt, tmp, len(que))
            else:
                tmp = [prunning[i].count(100) for i in range(4)]
                print(cnt, tmp, len(que))
            #print(prunning[0])
        status, num, l_mov, l2_mov = que.popleft()
        l_twist_0 = l_mov // 3
        l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
        l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
        for twist in successor[phase]:
            if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
                continue
            n_status = status.move(twist)
            idx = n_status.phase_idx(phase)
            if phase == 1:
                parity = n_status.sgn()
                if prunning[parity][idx] < 100:
                    continue
                prunning[parity][idx] = num + 1
                que.append([n_status, num + 1, twist, l_mov])
            else:
                if prunning[idx] < 100:
                    continue
                prunning[idx] = num + 1
                que.append([n_status, num + 1, twist, l_mov])

    if phase == 1:
        with open('prunning' + str(phase) + '.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for i in range(len(prunning)):
                writer.writerow(prunning[i])
    else:
        with open('prunning' + str(phase) + '.csv', mode='w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(prunning)

'''

'''
# phase1 FBUD center
prunning = [100 for _ in range(12870)] #cmb(16, 8)
prunning[solved.phase_idx(1)[0]] = 0
que = deque([[solved, 0, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 1000 == 0:
        tmp = prunning.count(100)
        print(cnt, tmp, len(que))
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
        if prunning[idx] > num + 1:
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning1.csv', mode='w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)
'''
'''
# phase1 RL center
prunning = [100 for _ in range(70)] #cmb(8, 4)
prunning[solved.phase_idx(1)[1]] = 0
que = deque([[solved, 0, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 1000 == 0:
        tmp = prunning.count(100)
        print(cnt, tmp, len(que))
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[1]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        idx = n_status.phase_idx(1)[1]
        if n_status.sgn() == 0:
            if prunning[idx] != 0:
                prunning[idx] = 0
                que.append([n_status, 0, -10, -10])
        elif prunning[idx] > num + 1:
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning1.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)
'''

'''
# phase1 low & high edges
prunning = [100 for _ in range(8388608)] #cmb(8, 4)
prunning[solved.phase_idx(1)[2]] = 0
que = deque([[solved, 0, -10, -10]])
cnt = 0
while que:
    cnt += 1
    if cnt % 1000 == 0:
        tmp = prunning.count(100)
        print(cnt, tmp, len(que))
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[1]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        idx = n_status.phase_idx(1)[2]
        if prunning[idx] > num + 1:
            prunning[idx] = num + 1
            que.append([n_status, num + 1, twist, l_mov])

with open('prunning1.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(prunning)
'''

'''
# phase2 1 Ce
prunning = [100 for _ in range(343000)]
que = deque([[solved, 0, -10, -10]])
cnt = 0
while que:
    strt = time()
    cnt += 1
    if cnt % 1000 == 0:
        tmp = prunning.count(100)
        print(cnt, tmp, len(que))
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
'''

# phase2 2 Ep
prunning = [[100 for _ in range(665280)] for _ in range(2)]
_, idx1, idx2 = solved.phase_idx(2)
prunning[0][idx1] = 0
prunning[0][idx2] = 0
que = deque([[solved, 0, -10, -10]])
cnt = 0
cnt1 = 0
cnt2 = 0
while que:
    cnt += 1
    if cnt % 1000 == 0:
        tmp = [prunning[i].count(100) for i in range(len(prunning))]
        print(cnt, cnt1, cnt2, tmp, len(que))
    status, num, l_mov, l2_mov = que.popleft()
    l_twist_0 = l_mov // 3
    l_twist_1 = l2_mov // 3 if l_mov // 12 == l2_mov // 12 else -10
    l_twist_2 = (l_mov // 3 + 2 if (l_mov // 3) % 4 == 1 else l_mov // 3 - 2) if (l_mov // 3) % 2 == 1 else -10
    for twist in successor[2]:
        if l_twist_0 == twist // 3 or l_twist_1 == twist // 3 or l_twist_2 == twist // 3:
            continue
        n_status = status.move(twist)
        _, idx1, idx2 = n_status.phase_idx(2)
        if n_status.edge_paired_4() and n_status.sgn_mod4() == 0:
            if prunning[0][idx1] != 0 or prunning[1][idx2] != 0:
                prunning[0][idx1] = 0
                prunning[1][idx2] = 0
                cnt1 += 1
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
                cnt2 += 1
                que.append([n_status, num + 1, twist, l_mov])

with open('prunning2.csv', mode='a') as f:
    writer = csv.writer(f, lineterminator='\n')
    for i in range(2):
        writer.writerow(prunning[i])



'''
# phase3 1 Ce
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


# phase3 1 Ep
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