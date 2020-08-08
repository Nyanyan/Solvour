'''
4x4x4 Solver Solver Part Written by Nyanyan
Copyright 2020 Nyanyan
'''

'''
Abstract:
* "X" twist includes X, X2, X', while "X2" means only X2
--- Reduction phase ---
phase 0: gather RL centers on RL faces
         use R, Rw, L, U, Uw, D, F, Fw, B
phase 1: gather FB centers on FB faces, separate low & high edges, make RL centers one of the 12 admissible state, avoid last two edges, clear OLL Parity
         use R, Rw, L, U, Uw2, D, F, Fw2, B
phase 2: make center columns and pair up 4 edges on the middle layer
         use R2, Rw2, L2, U, Uw2, D, F, Fw2, B
phase 3: complete centers, edges pairing and clear PLL Parity, which means complete reduction
         use R2, Rw2, L2, U, Uw2, D, F2, Fw2, B2
--- 3x3x3 phase ---
phase 4: gather UD stickers on UD faces and clear EO
         use R, L, U, D, F, B, not use R2, L2, F2, B2
phase 5: solve it!
         use R2, L2, U, D, F2, B2
'''

'''
Parts Numbering
        ---------
        |       |
        |   U   |
        | WHITE |
---------------------------------
|       |       |       |       |
|   L   |   F   |   R   |   B   |
| ORANGE| GREEN |  RED  |  BLUE |
---------------------------------
        |       |
        |   D   |
        | YELLOW|
        ---------

              ---------------
              |  0  0  1  1 |
              |  7  0  1  2 |
              |  6  3  2  3 |
              |  2  5  4  3 |
---------------------------------------------------------
|  0  7  6  2 |  2  5  4  3 |  3  3  2  1 |  1  1  0  0 |
| 15 16 17  8 |  8  4  5 11 | 11  8  9 12 | 12 12 13 15 |
| 14 19 18  9 |  9  7  6 10 | 10 11 10 13 | 13 15 14 14 |
|  6 22 23  4 |  4 16 17  5 |  5 18 19  7 |  7 20 21  6 |
---------------------------------------------------------
              |  4 16 17  5 |
              | 23 20 21 18 |
              | 22 23 22 19 |
              |  6 21 20  7 |
              ---------------
'''

'''
Color Numbering
        ---------
        |       |
        |   U   |
        |   0   |
---------------------------------
|       |       |       |       |
|   L   |   F   |   R   |   B   |
|   1   |   2   |   3   |   4   |
---------------------------------
        |       |
        |   D   |
        |   5   |
        ---------

              ---------------
              | 32 33 34 35 |
              | 36 37 38 39 |
              | 40 41 42 43 |
              | 44 45 46 47 |
---------------------------------------------------------
| 80 81 82 83 | 48 49 50 51 | 64 65 66 67 | 31 30 29 28 |
| 84 85 86 87 | 52 53 54 55 | 68 69 70 71 | 27 26 25 24 |
| 88 89 90 91 | 56 57 58 59 | 72 73 74 75 | 23 22 21 20 |
| 92 93 94 95 | 60 61 62 63 | 76 77 78 79 | 19 18 17 16 |
---------------------------------------------------------
              |  0  1  2  3 |
              |  4  5  6  7 |
              |  8  9 10 11 |
              | 12 13 14 15 |
              ---------------
'''

#from cube_class_c_6 import Cube, face, axis, wide, move_cp, move_co, move_ep, move_ce, move_candidate, twist_to_idx, successor, ep_switch_parity, idx_ep_phase1, idx_ep_phase2, ec_parity, ec_0_parity, skip_axis, reverse_move
from time import time
import numpy as np
cimport numpy as np
from math import sqrt

import csv
cimport cython

'''****************************************************** CLASS & FUNCTIONS PART ******************************************************'''

#                  0    1     2     3     4      5      6    7     8     9     10     11     12   13    14    15    16     17     18   19   20     21    22     23     24   25    26    27    28     29     30   31    32    33    34     35
move_candidate = ["R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "Lw", "Lw2", "Lw'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "Dw", "Dw2", "Dw'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'", "Bw", "Bw2", "Bw'"]
twist_to_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, -1, -1, -1, 9, 10, 11, 12, 13, 14, 15, 16, 17, -1, -1, -1, 18, 19, 20, 21, 22, 23, 24, 25, 26, -1, -1, -1]

successor = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14, 15, 16, 17, 18, 19, 20,             24, 25, 26, 27, 28, 29, 30, 31, 32            ], # phase 0
    [0, 1, 2, 3, 4, 5, 6, 7, 8,            12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            ], # phase 1
    [   1,       4,       7,               12, 13, 14,     16,     18, 19, 20,             24, 25, 26,     28,     30, 31, 32            ], # phase 2
    [   1,       4,       7,               12, 13, 14,             18, 19, 20,                 25,         28,         31,               ], # phase 3
    [0,    2,          6,    8,            12, 13, 14,             18, 19, 20,             24,     26,             30,     32            ], # phase 4
    [   1,                7,               12, 13, 14,             18, 19, 20,                 25,                     31                ]  # phase 5
    ]

skip_axis = [
    [3, 3, 3, 6, 6, 6, 9, 9, 9, 12, 12, 12, 15, 15, 15, 18, 18, 18, 21, 21, 21, 24, 24, 24, 27, 27, 27], # phase0
    [3, 3, 3, 6, 6, 6, 9, 9, 9, 12, 12, 12, 13, 16, 16, 16, 19, 19, 19, 20, 23, 23, 23], # phase1
    [1, 2, 3, 6, 6, 6, 7, 10, 10, 10, 13, 13, 13, 14, 17, 17, 17], # phase2
    [1, 2, 3, 6, 6, 6, 9, 9, 9, 10, 11, 12], # phase3
    [2, 2, 4, 4, 7, 7, 7, 10, 10, 10, 12, 12, 14, 14], # phase4
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
    
    def idx_ep_eo_phase4(self):
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
        cdef int[12] eo = [self.Ep[i] % 2 for i in range(0, 24, 2)]
        for i in range(11):
            res *= 2
            res += eo[i]
        return res

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

cdef ec_parity(ep, cp):
    cdef int res1 = pp_ep_p(ep, 0)
    cdef int res2 = pp_cp_p(cp, 0)
    return res1 % 2 != res2 % 2

cdef ec_0_parity(ep, cp):
    cdef int res1 = pp_ep_p(ep, 0)
    #cdef int res2 = pp_cp_p(cp, 0)
    return res1 % 2 != 0 #not(res1 % 2 == res2 % 2 == 0)

cdef pp_ep_p(arr, strt):
    cdef int i
    cdef int j
    for i in range(strt, 12):
        if arr[i] != i:
            for j in range(i, 12):
                if arr[j] == i:
                    arr[i], arr[j] = arr[j], arr[i]
                    return 1 + pp_ep_p(arr, i + 1)
    return 0

cdef pp_cp_p(arr, strt):
    cdef int i
    cdef int j
    for i in range(strt, 8):
        if arr[i] != i:
            for j in range(i, 8):
                if arr[j] == i:
                    arr[i], arr[j] = arr[j], arr[i]
                    return 1 + pp_cp_p(arr, i + 1)
    return 0

cdef ep_switch_parity(ep): # "last 2 edge"
    return ep_switch_parity_p([i for i in ep], 0, 0) % 2

cdef ep_switch_parity_p(arr, res, strt):
    cdef int i
    cdef int j
    for i in range(strt, 24):
        if arr[i] != i:
            for j in range(i + 1, 24):
                if arr[j] == i:
                    arr[i], arr[j] = arr[j], arr[i]
                    return ep_switch_parity_p(arr, res + 1, i + 1)
    return res

cdef ep_not_separate(ep):
    ep_even = {ep[i] // 2 for i in range(0, 24, 2)}
    if len(ep_even) < 12:
        return True
    return False

cdef eo_flip(ep):
    ep_even = [ep[i] % 2 for i in range(0, 24, 2)]
    res = sum(ep_even)
    return res

cdef idx_ep_phase2(ep):
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

cdef optimise(arr, int strt):
    if strt == len(arr) - 1:
        return arr
    if face(arr[strt]) == face(arr[strt + 1]):
        new_axis = arr[strt] // 3
        new_power = (arr[strt] % 3 + arr[strt + 1] % 3 + 2) % 4 - 1
        del arr[strt]
        if new_power == -1:
            del arr[strt]
        else:
            arr[strt] = new_axis * 3 + new_power
        return optimise(arr, strt)
    elif axis(arr[strt]) == axis(arr[strt + 1]):
        arr_copy = [i for i in arr]
        arr_copy[strt], arr_copy[strt + 1] = arr_copy[strt + 1], arr_copy[strt]
        res_1 = optimise(arr, strt + 1)
        res_2 = optimise(arr_copy, strt + 1)
        if len(res_1) < len(res_2):
            return res_1
        else:
            return res_2
    return optimise(arr, strt + 1)




'''****************************************************** SOLVER PART ******************************************************'''
#@cython.boundscheck(False)
#@cython.wraparound(False)
cdef initialize_puzzle_arr(int phase, puzzle):
    if phase == 0:
        return [puzzle.idx_ce_phase0()]
    elif phase == 1:
        return [puzzle.idx_ce_phase1_fbud() * 70 + puzzle.idx_ce_phase1_rl()]
    elif phase == 2:
        return [puzzle.idx_ce_phase23(), puzzle.Ep]
    elif phase == 3:
        return [puzzle.idx_ce_phase23(), puzzle.idx_ep_phase3()]
    elif phase == 4:
        return [puzzle.idx_co(), puzzle.idx_ep_eo_phase4()]
    elif phase == 5:
        return [puzzle.idx_cp(), puzzle.idx_ep_phase5()]

#@cython.boundscheck(False)
#@cython.wraparound(False)
cdef move_arr(puzzle_arr, int phase, int twist):
    cdef int tmp = twist_to_idx[twist]
    if phase == 0:
        return [move_ce_phase0[puzzle_arr[0]][tmp]]
    elif phase == 1:
        return [move_ce_phase1_fbud[puzzle_arr[0] // 70][tmp] * 70 + move_ce_phase1_rl[puzzle_arr[0] % 70][tmp]]
    elif phase == 2:
        return [move_ce_phase23[puzzle_arr[0]][tmp], move_ep(puzzle_arr[1], twist)]
    elif phase == 3:
        return [move_ce_phase23[puzzle_arr[0]][tmp], move_ep_phase3[puzzle_arr[1]][tmp]]
    elif phase == 4:
        return [move_co_arr[puzzle_arr[0]][tmp], move_ep_eo_phase4[puzzle_arr[1]][tmp]]
    elif phase == 5:
        return [move_cp_arr[puzzle_arr[0]][tmp], move_ep_phase5_ud[puzzle_arr[1] // 24][tmp] * 24 + move_ep_phase5_fbrl[puzzle_arr[1] % 24][tmp]]

#@cython.boundscheck(False)
#@cython.wraparound(False)
cdef nyanyan_function(lst):
    cdef int sm = sum(lst)
    cdef int mx = max(lst)
    cdef float mean = sm / len(lst)
    cdef float sd = 0
    cdef int i
    for i in lst:
        sd += (mean - i) ** 2
    sd = sqrt(sd)
    if sd == 0:
        return mx
    cdef float euclid = 0
    for i in lst:
        euclid += i ** 2
    euclid = sqrt(euclid)
    #cdef float ratio = max(1, min(0, (3 * (mx - 5) + sd) / 8))
    cdef float ratio = pow(2, -pow((mx / sd - 1.5), 4) / 2) # ratio is small when mx is near to constant and sd is small
    #print(mx, sd, ratio)
    return int(mx * (1 - ratio) + euclid * ratio)

#@cython.boundscheck(False)
#@cython.wraparound(False)
cdef distance(puzzle_arr, int phase):
    #global parity_cnt
    if phase == 2:
        lst = [prunning[phase][0][puzzle_arr[0]], None, None]
        idxes = idx_ep_phase2(puzzle_arr[1])
        for i in range(2):
            lst[i + 1] = prunning[phase][i + 1][idxes[i]]
    else:
        lst = [prunning[phase][i][puzzle_arr[i]] for i in range(prun_len[phase])]
    cdef int res = nyanyan_function(lst)
    cdef int[24] puzzle_ep
    cdef int[8] puzzle_cp
    cdef int[12] puzzle_ep_p
    if res == 0:
        puzzle_ep = [i for i in puzzle.Ep]
        puzzle_cp = [i for i in puzzle.Cp]
        for i in path:
            puzzle_ep = move_ep(puzzle_ep, i)
            puzzle_cp = move_cp(puzzle_cp, i)
        if phase == 1: # find OLL Parity (2 edge remaining)
            if ep_switch_parity(puzzle_ep) or ep_not_separate(puzzle_ep) or eo_flip(puzzle_ep) % 2:
                #parity_cnt += 1
                return 99
        elif phase == 3: # find PLL Parity
            puzzle_ep_p = [puzzle_ep[i] // 2 for i in range(0, 24, 2)]
            if ec_parity(puzzle_ep_p, puzzle_cp):
                #parity_cnt += 1
                return 99
        elif res == 0 and phase == 4: # adjust EO
            puzzle_ep_p = [puzzle_ep[i] // 2 for i in range(0, 24, 2)]
            if ec_0_parity(puzzle_ep_p, puzzle_cp):
                #parity_cnt += 1
                return 99
    return res

#@cython.boundscheck(False)
#@cython.wraparound(False)
cdef skip(int phase, int twist, int l1_twist, int l2_twist, int l3_twist):
    cdef int axis_twist = axis(twist)
    cdef int axis_l1_twist = axis(l1_twist)
    cdef int face_twist = face(twist)
    if axis_twist == axis_l1_twist and face_twist <= face(l1_twist):
        return True
    if phase < 4:
        if axis_twist == axis_l1_twist == axis(l2_twist) == axis(l3_twist) or (axis_twist == axis_l1_twist and face_twist == face(l2_twist)):
            return True
    elif phase >= 4:
        if axis_twist == axis_l1_twist == axis(l2_twist):
            return True
    return False

#@cython.boundscheck(False)
#@cython.wraparound(False)
cdef phase_search(int phase, puzzle_arr, int depth, int dis):
    global path, cnt
    cdef int l1_twist, l2_twist, l3_twist, twist_idx, len_successor, n_dis, twist
    if depth == 0:
        return dis == 0
    else:
        if dis == 0:
            return True
        l1_twist = path[-1] if len(path) >= 1 else -10
        l2_twist = path[-2] if len(path) >= 2 else -10
        l3_twist = path[-3] if len(path) >= 3 else -10
        twist_idx = 0
        len_successor = len(successor[phase])
        for _ in range(28):
            if twist_idx >= len_successor:
                return False
            twist = successor[phase][twist_idx]
            if skip(phase, twist, l1_twist, l2_twist, l3_twist):
                twist_idx = skip_axis[phase][twist_idx]
                continue
            #cnt += 1
            n_puzzle_arr = move_arr(puzzle_arr, phase, twist)
            path.append(twist)
            n_dis = distance(n_puzzle_arr, phase)
            if n_dis >= depth:
                path.pop()
                if n_dis > depth:
                    twist_idx = skip_axis[phase][twist_idx]
                    if n_dis == 99:
                        return False
                else:
                    twist_idx += 1
                continue
            if phase_search(phase, n_puzzle_arr, depth - 1, n_dis):
                return True
            path.pop()
            twist_idx += 1

def state_to_cube(state):
    res = Cube()
    corners = [[0, 4, 3], [0, 3, 2], [0, 1, 4], [0, 2, 1], [5, 4, 1], [5, 1, 2], [5, 3, 4], [5, 2, 3]]
    set_corners = [set(i) for i in corners]
    for idx, arr in enumerate([[32, 80, 28], [35, 31, 67], [44, 48, 83], [47, 64, 51], [0, 95, 60], [3, 63, 76], [12, 16, 92], [15, 79, 19]]):
        colors = [state[i] for i in arr]
        set_colors = set(colors)
        for i in range(8):
            if set_colors == set_corners[i]:
                res.Cp[idx] = i
                res.Co[idx] = colors.index(corners[i][0])
                break
        else:
            return -1
    if len(set(res.Cp)) != 8 or sum(res.Co) % 3:
        return -1
    edges = [[0, 3], [3, 0], [0, 2], [2, 0], [0, 1], [1, 0], [0, 4], [4, 0], [4, 1], [1, 4], [2, 1], [1, 2], [2, 3], [3, 2], [4, 3], [3, 4], [5, 1], [1, 5], [5, 2], [2, 5], [5, 3], [3, 5], [5, 4], [4, 5]]
    for idx, arr in enumerate([[33, 29], [30, 34], [39, 66], [65, 43], [46, 50], [49, 45], [40, 82], [81, 36], [87, 52], [56, 91], [72, 59], [55, 68], [71, 27], [23, 75], [88, 20], [24, 84], [1, 61], [62, 2], [7, 77], [78, 11], [14, 18], [17, 13], [8, 93], [94, 4]]):
        colors = [state[i] for i in arr]
        for i in range(24):
            if colors == edges[i]:
                res.Ep[idx] = i
                break
        else:
            return -1
    if len(set(res.Ep)) != 24:
        return -1
    centers = [37, 38, 42, 41, 53, 54, 58, 57, 69, 70, 74, 73, 26, 25, 21, 22, 85, 86, 90, 89, 5, 6, 10, 9]
    res.Ce = [state[i] for i in centers]
    if len(set(res.Ce)) != 6:
        return -1
    for i in range(6):
        if res.Ce.count(i) != 4:
            return -1
    return res

def solver(state):
    global path, cnt, puzzle, parity_cnt, puzzle
    puzzle = state_to_cube(state)
    if puzzle == -1:
        return 'Error'
    solution = []
    cdef int phase = 0
    cdef int dis, depth, twist
    while phase < 6:
        strt = time()
        puzzle_arr = initialize_puzzle_arr(phase, puzzle)
        dis = distance(puzzle_arr, phase)
        depth = dis
        while depth < 40:
            path = []
            if phase_search(phase, puzzle_arr, depth, dis):
                for twist in path:
                    puzzle = puzzle.move(twist)
                solution.extend(path)
                phase += 1
                break
            depth += 1
        else:
            print('phase', phase, 'failed!')
            return 'Error'
    solution = optimise(solution, 0)
    solution_str = ''
    for i in solution:
        solution_str += move_candidate[i] + ' '
    return solution_str

cdef int[735471][27] move_ce_phase0
cdef int[12870][27] move_ce_phase1_fbud
cdef int[70][27] move_ce_phase1_rl
cdef int[343000][27] move_ce_phase23
cdef int[40320][27] move_ep_phase3
cdef int[2187][27] move_co_arr
cdef int[1013760][27] move_ep_eo_phase4
cdef int[40320][27] move_cp_arr
cdef int[40320][27] move_ep_phase5_ud
cdef int[24][27] move_ep_phase5_fbrl
cdef int[6] prun_len = [1, 1, 3, 2, 2, 2]
prunning = [[[] for _ in range(prun_len[i])] for i in range(6)]

if __name__ == 'solver_c_5':
    global move_ce_phase0, move_ce_phase1_fbud, move_ce_phase1_rl, move_ce_phase23, move_ep_phase3, move_co_arr, move_ep_eo_phase4, move_cp_arr, move_ep_phase5_ud, move_ep_phase5_fbrl, prunning, prun_len
    print('getting moving array')
    with open('move/ce_phase0.csv', mode='r') as f:
        for idx in range(735471):
            move_ce_phase0[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ce_phase1_fbud.csv', mode='r') as f:
        for idx in range(12870):
            move_ce_phase1_fbud[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ce_phase1_rl.csv', mode='r') as f:
        for idx in range(70):
            move_ce_phase1_rl[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ce_phase23.csv', mode='r') as f:
        for idx in range(343000):
            move_ce_phase23[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ep_phase3.csv', mode='r') as f:
        for idx in range(40320):
            move_ep_phase3[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/co.csv', mode='r') as f:
        for idx in range(2187):
            move_co_arr[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ep_eo_phase4.csv', mode='r') as f:
        for idx in range(1013760):
            move_ep_eo_phase4[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/cp.csv', mode='r') as f:
        for idx in range(40320):
            move_cp_arr[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ep_phase5_ud.csv', mode='r') as f:
        for idx in range(40320):
            move_ep_phase5_ud[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.',end='',flush=True)
    with open('move/ep_phase5_fbrl.csv', mode='r') as f:
        for idx in range(24):
            move_ep_phase5_fbrl[idx] = [int(i) for i in f.readline().replace('\n', '').split(',')]
    #print('.')
    print('getting prunning array')
    for phase in range(6):
        #int*[prun_len[phase]] prunning[phase] = [[] for _ in range(prun_len[phase])]
        #prunning.append([])
        with open('prun/prunning' + str(phase) + '.csv', mode='r') as f:
            for lin in range(prun_len[phase]):
                prunning[phase][lin] = np.array([int(i) for i in f.readline().replace('\n', '').split(',')])
        #print('.',end='',flush=True)
    #print('')

puzzle = Cube()
path = []
