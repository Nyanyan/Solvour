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

'''
Solver:
* "X" twist includes X, X2, X', while "X2" means only X2
--- Reduction phase ---
phase 0: gather RL centers on RL faces
         use R, Rw, L, U, Uw, D, F, Fw, B
phase 1: gather FB centers on FB faces, separate low & high edges, clear RL center parity, avoid last two edges
         use R, Rw, L, U, Uw2, D, F, Fw2, B
phase 2: make center columns and pair up 4 edges on the middle layer
         use R2, Rw2, L2, U, Uw2, D, F, Fw2, B
phase 3: complete center, edge pairing and clear edge parity (= PP), which means complete reduction
         use R2, Rw2, L2, U, Uw2, D, F2, Fw2, B2
--- 3x3x3 phase ---
phase 4: gather UD stickers on UD faces and clear EO
         use R, L, U, D, F, B, not use R2, L2, F2, B2
phase 5: solve it!
         use R2, L2, U, D, F2, B2
'''


import tkinter
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
            return [res * 2 + self.ce_parity()]
        elif phase == 1:
            cnt = 0
            arr = [0, 1, 2, 3, 20, 21, 22, 23, 4, 5, 6, 7, 12, 13, 14, 15] # FBUD centers
            for i in range(15):
                if self.Ce[arr[i]] == 1 or self.Ce[arr[i]] == 3:
                    res += cmb(15 - i, 8 - cnt)
                    cnt += 1
                    if cnt == 8 or i - cnt == 7:
                        break
            res *= 70
            cnt = 0
            for i in range(7): # RL centers
                if self.Ce[rl_center[i]] == 4:
                    res += cmb(7 - i, 4 - cnt)
                    cnt += 1
                    if cnt == 4 or i - cnt == 3:
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
            for i in range(12):
                res3 *= 2
                if self.Ep[i] % 2 != i % 2:
                    res3 += 1
            res4 = 0
            for i in range(12, 24):
                res4 *= 2
                if self.Ep[i] % 2 != i % 2:
                    res4 += 1
            return res, res3, res4
        elif phase == 2:
            res0 = 0
            cnt = 0
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
            #tmp = [4, 5, 6, 7]
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
            for i in range(8):
                cnt = 0
                for j in arr3[i + 1:]:
                    if j < arr3[i]:
                        cnt += 1
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
                cnt = 0
                for j in self.Cp[:i]:
                    if j < self.Cp[i]:
                        cnt += 1
                res0 += fac[7 - i] * (self.Cp[i] - cnt)
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
    
    def pp_parity(self): # this is PP checker, if 1, there is PP, although not-proved
        #arr = [[self.Ep[i] // 2, False] for i in range(0, 24, 2)]
        '''
        for i in range(12):
            if arr[i][0] != i:
                for j in range(i + 1, 12):
                    if arr[j][0] == i:
                        arr[i][0], arr[j][0] = arr[j][0], arr[i][0]
                        res += 1
                        arr[j][1] = True
            elif arr[i][1]:
                res += 1
        '''
        ep = [self.Ep[i] // 2 for i in range(0, 24, 2)]
        cp = [i for i in self.Cp]
        res1 = pp_ep_p(ep, 0)
        res2 = pp_cp_p(cp, 0)
        #if (res1 + res2) % 2 == 0:
            #print(res1, res2)
            #print([self.Ep[i] // 2 for i in range(0, 24, 2)])
            #print(self.Cp)
            #return 0
        return (res1 + res2) % 2
    
    def ep_swich_parity(self): # avoid "last 2 edge"
        return ep_switch_parity_p([i for i in self.Ep], 0) % 2
    
    def check_eo(self):
        for i in range(0, 24, 2):
            if self.Ep[i] % 2:
                return True
        return False
    
    def ec_parity(self):
        '''
        corner = 0
        for i in range(8):
            cnt = self.Cp[i]
            for j in self.Cp[i + 1:]:
                if j < self.Cp[i]:
                    cnt -= 1
            corner += fac[7 - i] * (self.Cp[i] - cnt)
            corner %= 4
        edge = 0
        for i in range(12):
            cnt = self.Ep[i * 2] // 2
            for j in range(i):
                if self.Ep[j * 2] < self.Ep[i * 2]:
                    cnt -= 1
            edge += fac[11 - i] * cnt
            edge %= 4
        return not (corner == edge == 0)
        '''
        ep = [self.Ep[i] // 2 for i in range(0, 24, 2)]
        cp = [i for i in self.Cp]
        res1 = pp_ep_p(ep, 0)
        res2 = pp_cp_p(cp, 0)
        return not res1 % 4 == res2 % 4 == 0
    
    def distance(self, phase):
        idxes = self.phase_idx(phase)
        if phase == 1:
            parity = self.ep_swich_parity()
            return_val = max(prunning[phase][0][idxes[0]], prunning[phase][1 + parity][idxes[1]], prunning[phase][3 + parity][idxes[2]])
        elif phase == 3:
            return_val = max(prunning[phase][0][idxes[0]], prunning[phase][1 + self.pp_parity()][idxes[1]])
        elif phase == 4:
            parity = self.ec_parity()
            return_val = max(prunning[phase][parity][idxes[0]], prunning[phase][2 + parity][idxes[1]])
        else:
            return_val = max([prunning[phase][i][idxes[i]] for i in range(len(idxes))])

        '''
        if phase == 1 and return_val < 2:
            print([prunning[phase][i][idxes[i]] for i in range(len(idxes))])
            print(idxes)
            #print(return_val)
            #print(self.Ce)
        '''
        return return_val

def pp_ep_p(arr, res):
    for i in range(12):
        if arr[i] != i:
            for j in range(12):
                if arr[j] == i:
                    arr[i], arr[j] = arr[j], arr[i]
                    res += 1
                    return pp_ep_p(arr, res)
    return res

def pp_cp_p(arr, res):
    for i in range(8):
        if arr[i] != i:
            for j in range(8):
                if arr[j] == i:
                    arr[i], arr[j] = arr[j], arr[i]
                    res += 1
                    return pp_cp_p(arr, res)
    return res

def ep_switch_parity_p(arr, res):
    for i in range(24):
        if arr[i] != i:
            for j in range(i + 1, 24):
                if arr[j] == i:
                    arr[i], arr[j] = arr[j], arr[i]
                    return ep_switch_parity_p(arr, res + 1)
    return res

def cmb(n, r):
    return fac[n] // fac[r] // fac[n - r]


def phase_search(phase, puzzle, depth):
    global path
    #print([move_candidate[i] for i in path], depth - puzzle.distance(phase))
    #if phase  == 3:
        #print(depth - puzzle.distance(phase))
    if depth == 0:
        if puzzle.distance(phase) == 0:
            return True
    else:
        if puzzle.distance(phase) <= depth:
            l_twist_0 = path[-1] // 3 if len(path) else -10
            l_twist_1 = path[-2] // 3 if len(path) >= 2 and path[-1] // 12 == path[-2] // 12 else -10
            l_twist_2 = (path[-1] // 3 + 2 if (path[-1] // 3) % 4 == 1 else path[-1] // 3 - 2) if len(path) and (path[-1] // 3) % 2 == 1 else -10
            for twist in successor[phase]:
                if twist // 3 == l_twist_0 or twist // 3 == l_twist_1 or twist // 3 == l_twist_2:
                    continue
                n_puzzle = puzzle.move(twist)
                path.append(twist)
                if phase_search(phase, n_puzzle, depth - 1):
                    return True
                path.pop()

def solver(puzzle):
    global solution, path
    solution = []
    for phase in range(6):
        print('phase', phase, 'depth', end=' ',flush=True)
        strt = time()
        for depth in range(20):
            print(depth, end=' ', flush=True)
            path = []
            if phase_search(phase, puzzle, depth):
                for twist in path:
                    puzzle = puzzle.move(twist)
                solution.extend(path)
                #print('phase', phase, end=': ')
                print('')
                for i in path:
                    print(move_candidate[i], end=' ')
                print('')
                print(time() - strt, 'sec')
                break

fac = [1 for _ in range(25)]
for i in range(1, 25):
    fac[i] = fac[i - 1] * i

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

prunning = [None for _ in range(8)]
prun_len = [1, 5, 3, 3, 4, 3]
for phase in range(6):
    prunning[phase] = [[] for _ in range(prun_len[phase])]
    with open('prunning' + str(phase) + '.csv', mode='r') as f:
        for lin in range(prun_len[phase]):
            prunning[phase][lin] = [int(i) for i in f.readline().replace('\n', '').split(',')]

solution = []
path = []
scramble = [move_candidate.index(i) for i in input("scramble: ").split()]
puzzle = Cube()
for mov in scramble:
    puzzle = puzzle.move(mov)
solver(puzzle)
print('solution:',end=' ')
#print(solution)
for i in solution:
    print(move_candidate[i],end=' ')
print('')
print(len(solution), 'moves')





