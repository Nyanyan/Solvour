'''
Corner
   B
  0 1 
L 2 3 R
   F

   F
  4 5
L 6 7 R
   B


Edge
top layer
    B
   0 1
  7   2
L 6   3 R
   5 4
    F

Middle layer
8   11   12   15
9 F 10 R 13 B 14

Bottom layer
     F
   16 17
  23   18
L 22   19 R
   21 20
     B


Center
top layer
   B
  0 1 
L 2 3 R
   F

Middle layer
4   5   8    9  12   13  16   17
7 F 6  11 R 10  15 B 14  19 L 18

Bottom layer
    F
  20 21
L 23 22 R
    B
'''
cimport numpy as np
cimport numpy as np
cimport cython

#                  0    1     2     3     4      5      6    7     8     9     10     11     12   13    14    15    16     17     18   19   20     21    22     23     24   25    26    27    28     29     30   31    32    33    34     35
move_candidate = ["R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "Lw", "Lw2", "Lw'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "Dw", "Dw2", "Dw'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'", "Bw", "Bw2", "Bw'"]
twist_to_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, -1, -1, -1, 9, 10, 11, 12, 13, 14, 15, 16, 17, -1, -1, -1, 18, 19, 20, 21, 22, 23, 24, 25, 26, -1, -1, -1]

successor = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14, 15, 16, 17, 18, 19, 20,             24, 25, 26, 27, 28, 29, 30, 31, 32            ], # phase 0
    [0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            ], # phase 1
    [   1,       4,       7,               12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            ], # phase 2
    [   1,       4,       7,               12, 13, 14,             18, 19, 20,                 25,         28,         31,               ], # phase 3
    [                                      12, 13, 14,             18, 19, 20,             24,     26,             30,     32            ], # phase 4
    [   1,                7,               12, 13, 14,             18, 19, 20,                 25,                     31                ]  # phase 5
    ]

skip_axis = [
    [3, 3, 3, 6, 6, 6, 9, 9, 9, 12, 12, 12, 15, 15, 15, 18, 18, 18, 21, 21, 21, 24, 24, 24, 27, 27, 27], # phase0
    [3, 3, 3, 6, 6, 6, 9, 9, 9, 12, 12, 12, 13, 16, 16, 16, 19, 19, 19, 20, 23, 23, 23], # phase1
    [1, 2, 3, 6, 6, 6, 7, 10, 10, 10, 13, 13, 13, 14, 17, 17, 17], # phase2
    [1, 2, 3, 6, 6, 6, 9, 9, 9, 10, 11, 12], # phase3
    [3, 3, 3, 6, 6, 6, 8, 8, 10, 10], # phase4
    [1, 2, 5, 5, 5, 8, 8, 8, 9, 10] # phase5
    ]

cdef int[8] rl_center = [8, 9, 10, 11, 16, 17, 18, 19]
cdef int[8] fb_center = [4, 5, 6, 7, 12, 13, 14, 15]
cdef int[8] ud_center = [0, 1, 2, 3, 20, 21, 22, 23]

fac = [1 for _ in range(25)]
for i in range(1, 25):
    fac[i] = fac[i - 1] * i

cdef cmb(n, r):
    return fac[n] // fac[r] // fac[n - r]

cdef face(int twist):
    return twist // 3

cdef axis(int twist):
    return twist // 12

cdef wide(int twist):
    return (twist // 3) % 2


cdef move_cp(arr, mov):
    cdef int[6][4] surface = [[3, 1, 7, 5], [0, 2, 4, 6], [0, 1, 3, 2], [4, 5, 7, 6], [2, 3, 5, 4], [1, 0, 6, 7]]
    cdef int[3][4] shift = [[1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]
    cdef int[8] res = [i for i in arr]
    cdef int mov_type = mov // 6
    cdef int mov_amount = mov % 3
    cdef int i
    for i in range(4):
        res[surface[mov_type][shift[mov_amount][i]]] = arr[surface[mov_type][i]]
    return res

cdef move_co(arr, mov):
    cdef int[6][4] surface = [[3, 1, 7, 5], [0, 2, 4, 6], [0, 1, 3, 2], [4, 5, 7, 6], [2, 3, 5, 4], [1, 0, 6, 7]]
    cdef int[4] pls = [2, 1, 2, 1]
    cdef int[3][4] shift = [[1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]
    cdef int[8] res = [i for i in arr]
    cdef int mov_type = mov // 6
    cdef int mov_amount = mov % 3
    cdef int i
    for i in range(4):
        res[surface[mov_type][shift[mov_amount][i]]] = arr[surface[mov_type][i]]
        if mov_type // 2 != 1 and mov_amount != 1:
            res[surface[mov_type][shift[mov_amount][i]]] += pls[shift[mov_amount][i]]
            res[surface[mov_type][shift[mov_amount][i]]] %= 3
    return res

cdef move_ep(arr, mov):
    surface = [
        [[3, 12, 19, 10], [2, 13, 18, 11]], # R
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
    cdef int[3][4] shift = [[1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]
    cdef int mov_type = mov // 3
    cdef int mov_amount = mov % 3
    cdef int[24] res = [i for i in arr]
    cdef int i
    for m_surface in surface[mov_type]:
        for i in range(4):
            res[m_surface[shift[mov_amount][i]]] = arr[m_surface[i]]
    return res

cdef move_ce(arr, mov):
    surface = [
        [[8, 9, 10, 11]], # R
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
    cdef int[3][4] shift = [[1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]
    cdef int mov_type = mov // 3
    cdef int mov_amount = mov % 3
    cdef int[24] res = [i for i in arr]
    cdef int i
    for m_surface in surface[mov_type]:
        for i in range(4):
            res[m_surface[shift[mov_amount][i]]] = arr[m_surface[i]]
    return res

class Cube:
    def __init__(self, cp=list(range(8)), co=[0 for _ in range(8)], ep=list(range(24)), ce=[i // 4 for i in range(24)]):
        self.Cp = cp
        self.Co = co
        self.Ep = ep
        self.Ce = ce
    
    def move(self, mov):
        return Cube(cp=move_cp(self.Cp, mov), co=move_co(self.Co, mov), ep=move_ep(self.Ep, mov), ce=move_ce(self.Ce, mov))

    def idx_cp(self):
        cdef int res = 0
        cdef int i
        cdef int j
        for i in range(8):
            cnt = self.Cp[i]
            for j in self.Cp[:i]:
                if j < self.Cp[i]:
                    cnt -= 1
            res += fac[7 - i] * cnt
        return res
    
    def idx_co(self):
        cdef int res = 0
        cdef int i
        for i in range(7):
            res *= 3
            res += self.Co[i]
        return res

    def idx_ce_phase0(self):
        cdef int res = 0
        cdef int cnt = 0
        cdef int i
        for i in range(23):
            if self.Ce[i] == 2 or self.Ce[i] == 4:
                res += cmb(23 - i, 8 - cnt)
                cnt += 1
                if cnt == 8 or i - cnt == 15:
                    break
        return res

    def idx_ce_phase1_fbud(self):
        cdef int res = 0
        cdef int cnt = 0
        cdef int[16] arr = [0, 1, 2, 3, 20, 21, 22, 23, 4, 5, 6, 7, 12, 13, 14, 15] # FBUD centers
        cdef int i
        for i in range(15):
            if self.Ce[arr[i]] == 1 or self.Ce[arr[i]] == 3:
                res += cmb(15 - i, 8 - cnt)
                cnt += 1
                if cnt == 8 or i - cnt == 7:
                    break
        return res
    
    def idx_ce_phase1_rl(self):
        cdef int res = 0
        cdef int cnt = 0
        cdef int i
        for i in range(7): # RL centers
            if self.Ce[rl_center[i]] == 4:
                res += cmb(7 - i, 4 - cnt)
                cnt += 1
                if cnt == 4 or i - cnt == 3:
                    break
        return res
    
    def idx_ce_phase23(self):
        cdef int res = 0
        cdef int cnt = 0
        cdef int i
        for i in range(7):
            if self.Ce[rl_center[i]] == 4:
                res += cmb(7 - i, 4 - cnt)
                cnt += 1
                if cnt == 4 or i - cnt == 3:
                    break
        res *= 70
        cnt = 0
        for i in range(7):
            if self.Ce[fb_center[i]] == 3:
                res += cmb(7 - i, 4 - cnt)
                cnt += 1
                if cnt == 4 or i - cnt == 3:
                    break
        res *= 70
        cnt = 0
        for i in range(7):
            if self.Ce[ud_center[i]] == 5:
                res += cmb(7 - i, 4 - cnt)
                cnt += 1
                if cnt == 4 or i - cnt == 3:
                    break
        return res

    
    def idx_ep_phase3(self):
        cdef int[8] arr1 = [self.Ep[i] // 2 for i in [1, 3, 5, 7, 17, 19, 21, 23]]
        cdef int[8] arr2 = [self.Ep[i] // 2 for i in [0, 2, 4, 6, 16, 18, 20, 22]]
        cdef int[8] arr3
        cdef int i
        cdef int j
        cdef int cnt
        for i in range(8):
            arr3[i] = arr2.index(arr1[i])
        cdef int res = 0
        for i in range(8):
            cnt = arr3[i]
            for j in arr3[:i]:
                if j < arr3[i]:
                    cnt -= 1
            res += cnt * fac[7 - i]
        return res
    
    def idx_ep_phase4(self):
        cdef int[12] ep = [self.Ep[i] // 8 for i in range(0, 24, 2)]
        cdef int res = 0
        cdef int remain = 4
        cdef int i
        for i in range(12):
            if ep[i] == 1:
                res += cmb(11 - i, remain)
                remain -= 1
                if remain == 0:
                    break
        return res
    '''
    def idx_eo_phase4(self):
        ep = [self.Ep[i] % 2 for i in range(0, 24, 2)]
        res = 0
        for i in range(12):
            res *= 2
            res += ep[i]
        return res
    '''

    def idx_ep_phase5_ud(self):
        cdef int[8] ud = [self.Ep[i] // 2 for i in [0, 2, 4, 6, 16, 18, 20, 22]]
        cdef int i
        cdef int j
        for i in range(8):
            if ud[i] >= 8:
                ud[i] -= 4
        cdef int res_ud = 0
        for i in range(8):
            cnt = ud[i]
            for j in ud[:i]:
                if j < ud[i]:
                    cnt -= 1
            res_ud += fac[7 - i] * cnt
        return res_ud
    
    def idx_ep_phase5_fbrl(self):
        cdef int[4] fbrl = [self.Ep[i] // 2 - 4 for i in [8, 10, 12, 14]]
        cdef int res_fbrl = 0
        cdef int i
        cdef int j
        cdef int cnt
        for i in range(4):
            cnt = fbrl[i]
            for j in fbrl[:i]:
                if j < fbrl[i]:
                    cnt -= 1
            res_fbrl += fac[3 - i] * cnt
        return res_fbrl
    
    def idx_ep_phase5(self):
        return self.idx_ep_phase5_ud() * 24 + self.idx_ep_phase5_fbrl()

    
    def ce_parity(self):
        cdef int[4][2] arr = [[8, 11], [9, 10], [16, 19], [17, 18]]
        for m_arr in arr:
            if self.Ce[m_arr[0]] != self.Ce[m_arr[1]]:
                return 1
        return 0
    
    def iscolumn(self):
        cdef int[8][2] arr = [[4, 7], [5, 6], [8, 11], [9, 10], [12, 15], [13, 14], [16, 19], [17, 18]]
        for m_arr in arr:
            if self.Ce[m_arr[0]] != self.Ce[m_arr[1]]:
                return False
        return True
    
    def low_high_separated(self):
        cdef int i
        for i in range(24):
            if self.Ep[i] % 2 != i % 2:
                return False
        return True
    
    def edge_paired_4(self):
        cdef int i
        for i in range(4, 8):
            if self.Ep[i * 2] // 2 != self.Ep[i * 2 + 1] // 2:
                return False
        return True

def ec_parity(ep, cp):
    cdef int res1 = pp_ep_p(ep, 0)
    cdef int res2 = pp_cp_p(cp, 0)
    return res1 % 2 != res2 % 2

def ec_0_parity(ep, cp):
    cdef int res1 = pp_ep_p(ep, 0)
    #cdef int res2 = pp_cp_p(cp, 0)
    return res1 % 2 != 0 #not(res1 % 2 == res2 % 2 == 0)

def pp_ep_p(arr, strt):
    cdef int i
    cdef int j
    for i in range(strt, 12):
        if arr[i] != i:
            for j in range(i, 12):
                if arr[j] == i:
                    arr[i], arr[j] = arr[j], arr[i]
                    return 1 + pp_ep_p(arr, i + 1)
    return 0

def pp_cp_p(arr, strt):
    cdef int i
    cdef int j
    for i in range(strt, 8):
        if arr[i] != i:
            for j in range(i, 8):
                if arr[j] == i:
                    arr[i], arr[j] = arr[j], arr[i]
                    return 1 + pp_cp_p(arr, i + 1)
    return 0

def idx_ep_phase1(ep):
    cdef int res = 0
    cdef int[24] arr = [i % 2 for i in ep]
    cdef int remain_1 = 12
    cdef int i
    for i in range(24):
        if arr[i] == 1:
            res += cmb(23 - i, remain_1)
            remain_1 -= 1
            if remain_1 == 0 or i + remain_1 == 23:
                break
    return res

def ep_switch_parity(ep): # "last 2 edge"
    return ep_switch_parity_p([i for i in ep], 0, 0) % 2

def ep_switch_parity_p(arr, res, strt):
    cdef int i
    cdef int j
    for i in range(strt, 24):
        if arr[i] != i:
            for j in range(i + 1, 24):
                if arr[j] == i:
                    arr[i], arr[j] = arr[j], arr[i]
                    return ep_switch_parity_p(arr, res + 1, i + 1)
    return res

def idx_ep_phase2(ep):
    cdef int[12] arr1 = [ep[i] // 2 for i in range(1, 24, 2)]
    cdef int[12] arr2 = [ep[i] // 2 for i in range(0, 23, 2)]
    cdef int[12] arr3 = [-1 for _ in range(12)]
    cdef int i
    cdef int j
    for i in range(12):
        arr3[i] = arr2.index(arr1[i])
    #print(arr3)
    cdef int res1 = 0
    for i in range(6):
        cnt = arr3[i]
        for j in arr3[:i]:
            if j < arr3[i]:
                cnt -= 1
        res1 += cnt * cmb(11 - i, 5 - i) * fac[5 - i]
    #print(res1)
    cdef int res2 = 0
    for i in range(6, 12):
        cnt = arr3[i]
        for j in arr3[6:i]:
            if j < arr3[i]:
                cnt -= 1
        res2 += cnt * cmb(11 - i + 6, 5 - i + 6) * fac[5 - i + 6]
    return [res1, res2]



def reverse_move(arr):
    res = list(reversed(arr))
    for i in range(len(res)):
        tmp = res[i] % 3
        if tmp == 0:
            res[i] += 2
        elif tmp == 2:
            res[i] -= 2
    return res
