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

import tkinter
from time import time
import pandas as pd

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
            return [res]
        elif phase == 1:
            cnt = 0
            arr = [0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23] # FBUD centers
            for i in range(15):
                if self.Ce[arr[i]] == 1 or self.Ce[arr[i]] == 3:
                    res += cmb(15 - i, 8 - cnt)
                    cnt += 1
                    if cnt == 8 or i - cnt == 7:
                        break
            res2 = 0
            cnt = 0
            arr = [8, 9, 10, 11, 16, 17, 18, 19] # RL centers
            for i in range(8):
                if self.Ce[arr[i]] == 2:
                    res2 += cmb(7 - i, 4 - cnt)
                    cnt += 1
                    if cnt == 4 or i - cnt == 3:
                        break
            res3 = 0
            for i in range(23): # low & high edge
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
            arr3 = [-1 for _ in range(8)]
            for i in range(8):
                arr3[i] = arr2_p.index(arr1_p[i])
            print(arr3)
            for i in range(7):
                cnt = arr3[i]
                for j in arr3[i + 1:]:
                    if j < arr3[i]:
                        cnt -= 1
                res1 += fac[7 - i] * (arr3[i] - cnt)
            return res0, res1

    def distance(self, phase):
        idxes = self.phase_idx(phase)
        '''
        if phase == 3:
            print([prunning[phase][i][idxes[i]] for i in range(len(idxes))])
            print(idxes)
        '''
        return max([prunning[phase][i][idxes[i]] for i in range(len(idxes))])

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

'''
phase 0: gather RL centers on RL faces
phase 1: gather FB centers on FB faces, clear edge and center parity and make low edge to low place, high to high
phase 2: make center column and pair up 4 edges on middle layer
phase 3: complete center and edge pairing
'''

def solver(puzzle):
    global solution, path
    solution = []
    for phase in range(4):
        strt = time()
        for depth in range(20):
            #print(depth)
            path = []
            if phase_search(phase, puzzle, depth):
                for twist in path:
                    puzzle = puzzle.move(twist)
                #print('')
                print('phase', phase, end=' ')
                for i in path:
                    print(move_candidate[i], end=' ')
                solution.extend(path)
                break
        print(time() - strt)
        #print('OP:', puzzle.sgn())

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
            ]

prunning = [None for _ in range(8)]
for phase in range(4):
    line_len = 0
    with open('prunning' + str(phase) + '.csv', mode='r') as f:
        for line in f:
            line_len += 1
    prunning[phase] = [[] for _ in range(line_len)]
    with open('prunning' + str(phase) + '.csv', mode='r') as f:
        for lin in range(line_len):
            prunning[phase][lin] = [int(i) for i in f.readline().replace('\n', '').split(',')]

solution = []
path = []
scramble = [move_candidate.index(i) for i in input("scramble: ").split()]
puzzle = Cube()
for mov in scramble:
    puzzle = puzzle.move(mov)
solver(puzzle)
print(solution)






