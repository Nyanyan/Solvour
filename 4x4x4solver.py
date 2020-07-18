'''
Corner:
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
8   10   12   14
9 F 11 R 13 B 15

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
from collections import deque
from time import time

class Cube:
    def __init__(self):
        self.Cp = [i for i in range(8)]
        self.Co = [0 for _ in range(8)]
        self.Ep = [i for i in range(24)]
        self.Ce = [i // 4 for i in range(24)]
    
    def move_cp(self, mov):
        surface = [[3, 1, 7, 5], [3, 1, 7, 5], [0, 2, 4, 6], [0, 1, 3, 2], [0, 1, 3, 2], [4, 5, 7, 6], [2, 3, 5, 4], [2, 3, 5, 4], [1, 0, 6, 7]]
        res = [i for i in self.Cp]
        mov_type = mov // 3
        mov_amount = mov % 3
        for i in range(4):
            res[surface[mov_type][(i + mov_amount + 1) % 4]] = self.Cp[surface[mov_type][i]]
        return res
    
    def move_co(self, mov):
        surface = [[3, 1, 7, 5], [3, 1, 7, 5], [0, 2, 4, 6], [0, 1, 3, 2], [0, 1, 3, 2], [4, 5, 7, 6], [2, 3, 5, 4], [2, 3, 5, 4], [1, 0, 6, 7]]
        pls = [1, 2, 1, 2]
        res = [i for i in self.Co]
        mov_type = mov // 3
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
                   [[0, 2, 4, 6], [1, 3, 5, 7]], # U
                   [[0, 2, 4, 6], [1, 3, 5, 7], [14, 12, 10, 8]], # Uw
                   [[16, 18, 20, 22], [17, 19, 21, 23]], # D
                   [[5, 10, 17, 9], [4, 11, 16, 8]], # F
                   [[5, 10, 17, 9], [4, 11, 16, 8], [6, 3, 18, 23]], # Fw
                   [[1, 14, 21, 13], [0, 15, 20, 12]]] # B
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
                   [[0, 1, 2, 3]], # U
                   [[0, 1, 2, 3], [13, 9, 5, 17], [12, 8, 4, 16]], # Uw
                   [[20, 21, 22, 23]], # D
                   [[4, 5, 6, 7]], # F
                   [[4, 5, 6, 7], [3, 8, 21, 18], [2, 11, 20, 17]], # Fw
                   [[12, 13, 14, 15]] # B
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
    
    def ce_phase1_idx(self):
        res = 0
        cnt = 0
        for i in reversed(range(24)):
            if self.Ce[i] == 2 or self.Ce[i] == 4:
                cnt += 1
                res += cmb(23 - i, cnt)
        return res
    
    def ce_phase2_idx(self):
        res = 0
        cnt = 0
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23]
        for i in reversed(range(16)):
            if self.Ce[arr[i]] == 1 or self.Ce[arr[i]] == 3:
                cnt += 1
                res += cmb(15 - i, cnt)
        return res
    
    def ce_phase3_idx(self):
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
    

def cmb(n, r):
    return fac[n] // fac[r] // fac[n - r]

# gather RL centers
def phase_1(status, depth):
    global ans, puzzle
    l_mov_type = ans[0][-1] // 3 if ans[0] else -10
    l3_mov_type = ans[0][-1] // 9 if len(ans[0]) >= 3 and ans[0][-1] // 9 == ans[0][-2] // 9 == ans[0][-3] else -10
    lst = [0, 2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 20, 21, 23, 24, 26]
    for mov in lst:
        if l_mov_type == mov // 3 or l3_mov_type == mov // 9:
            continue
        n_status = status.move(mov)
        if len(ans[0]) + 1 + ce_phase1[n_status.ce_phase1_idx()] > depth:
            continue
        ans[0].append(mov)
        if len(ans[0]) == depth:
            if set([n_status.Ce[i] for i in rl_center]) == set([2, 4]):
                puzzle = n_status
                return True
            else:
                ans[0].pop()
        elif phase_1(n_status, depth):
            return True
        else:
            ans[0].pop()
    return False

# gather FB centers, clear parity
def phase_2(status, depth):
    global ans, puzzle
    l_mov_type = ans[1][-1] // 3 if ans[1] else -10
    l3_mov_type = ans[1][-1] // 9 if len(ans[1]) >= 3 and ans[1][-1] // 9 == ans[1][-2] // 9 == ans[1][-3] else -10
    lst = [0, 2, 3, 5, 6, 8, 9, 11, 13, 15, 17, 18, 20, 22, 24, 26]
    for mov in lst:
        if l_mov_type == mov // 3 or l3_mov_type == mov // 9:
            continue
        n_status = status.move(mov)
        if len(ans[1]) + 1 + ce_phase2[n_status.ce_phase2_idx()] > depth:
            continue
        ans[1].append(mov)
        if len(ans[1]) == depth:
            if set([n_status.Ce[i] for i in fb_center]) == set([1, 3]) and n_status.sgn_ep() == 0:
                puzzle = n_status
                return True
            else:
                ans[1].pop()
        elif phase_2(n_status, depth):
            return True
        else:
            ans[1].pop()
    return False

# pair up edges, complete centers = complete reduction
def phase_3(status, depth):
    global ans, puzzle
    l_mov_type = ans[2][-1] // 3 if ans[2] else -10
    l3_mov_type = ans[2][-1] // 9 if len(ans[2]) >= 3 and ans[2][-1] // 9 == ans[2][-2] // 9 == ans[2][-3] else -10
    lst = [0, 2, 4, 6, 8, 9, 11, 13, 15, 17, 18, 20, 22, 24, 26]
    for mov in lst:
        if l_mov_type == mov // 3 or l3_mov_type == mov // 9:
            continue
        n_status = status.move(mov)
        parity_idx = n_status.parity()
        if len(ans[2]) + 1 + max(ce_phase3[n_status.ce_phase3_idx()], parity_phase2_1[parity_idx[0]], parity_phase2_2[parity_idx[1]]) > depth:
            continue
        ans[2].append(mov)
        if len(ans[2]) == depth:
            flag = True
            for arr in edges:
                tmp = [n_status.Ep[i] for i in arr]
                if abs(tmp[0] - tmp[1]) != 1 or min(tmp) % 2:
                    flag = False
                    break
            for surface in range(5):
                if set([n_status.Ce[i] for i in range(surface * 4, surface * 4 + 4)]) != set([surface]):
                    flag = False
                    break
            if flag and parity_idx == (0, 0):
                puzzle = n_status
                return True
            else:
                ans[2].pop()
        elif phase_3(n_status, depth):
            return True
        else:
            ans[2].pop()
    return False
'''
# pair up remaining edges, solve centers
def phase_4(status, depth):
    global ans, puzzle
    l_mov_type = ans[-1] // 3 if ans else -10
    l3_mov_type = ans[-1] // 9 if len(ans) >= 3 and ans[-1] // 9 == ans[-2] // 9 == ans[-3] else -10
    lst = [1, 4, 7, 9, 11, 15, 17, 19, 22, 25]
    for mov in lst:
        if l_mov_type == mov // 3 or l3_mov_type == mov // 9:
            continue
        n_status = status.move(mov)
        ans.append(mov)
        if len(ans) == depth:
            flag_phase4 = True
            for arr in phase4_edges:
                tmp = [n_status.Ep[i] for i in arr]
                if abs(tmp[0] - tmp[1]) != 1 or min(tmp) % 2:
                    flag_phase4 = False
                    break
            if flag_phase4 and [n_status.Ce[i] for i in rl_center] == [2, 2, 2, 2, 4, 4, 4, 4] and [n_status.Ce[i] for i in fb_center] == [1, 1, 1, 1, 3, 3, 3, 3] and [n_status.Ce[i] for i in ud_center] == [0, 0, 0, 0, 5, 5, 5, 5]:
                puzzle = n_status
                return True
            else:
                ans.pop()
        elif phase_4(n_status, depth):
            return True
        else:
            ans.pop()
    return False
'''
fac = [1 for _ in range(25)]
for i in range(1, 25):
    fac[i] = fac[i - 1] * i

#                  0    1     2     3     4      5      6    7     8     9    10    11    12    13     14     15   16    17    18   19    20    21    22     23     24   25    26
move_candidate = ["R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'"]
rl_center = [8, 9, 10, 11, 16, 17, 18, 19]
fb_center = [4, 5, 6, 7, 12, 13, 14, 15]
ud_center = [0, 1, 2, 3, 20, 21, 22, 23]


with open('ce_phase1.csv', mode='r') as f:
    ce_phase1 = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('ce_phase2.csv', mode='r') as f:
    ce_phase2 = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('parity_phase2_1.csv', mode='r') as f:
    parity_phase2_1 = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('parity_phase2_2.csv', mode='r') as f:
    parity_phase2_2 = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('ce_phase3.csv', mode='r') as f:
    ce_phase3 = [int(i) for i in f.readline().replace('\n', '').split(',')]

ans = [[], [], [], [], []]
scramble = [move_candidate.index(i) for i in input("scramble: ").split()]
puzzle = Cube()
for mov in scramble:
    puzzle = puzzle.move(mov)
print('parity:', puzzle.parity())
print('sgn', puzzle.sgn_ep())
strt = time()

# phase 1
if set([puzzle.Ce[i] for i in rl_center]) != set([2, 4]):
    for depth in range(1, 9):
        if phase_1(puzzle, depth):
            break

print('phase 1',end=' ')
for i in ans[0]:
    print(move_candidate[i], end=' ')
print('')
print(time() - strt)

# phase 2
if set([puzzle.Ce[i] for i in fb_center]) != set([1, 3]) or puzzle.sgn_ep():
    for depth in range(1, 15):
        if phase_2(puzzle, depth):
            break

print('phase 2',end=' ')
for i in ans[1]:
    print(move_candidate[i], end=' ')
print('')
print(time() - strt)

# phase 3
edges = [[i * 2, i * 2 + 1] for i in range(12)]
flag_phase3 = True
for arr in edges:
    tmp = [puzzle.Ep[i] for i in arr]
    if abs(tmp[0] - tmp[1]) != 1 or min(tmp) % 2:
        flag_phase3 = False
        break
if (not flag_phase3) or puzzle.parity() != (0, 0):
    for depth in range(1, 17):
        if phase_3(puzzle, depth):
            break
print(puzzle.parity())

print('phase 3',end=' ')
for i in ans[2]:
    print(move_candidate[i], end=' ')
print('')
print(time() - strt)
'''
# phase 4
ud_center = [0, 1, 2, 3, 20, 21, 22, 23]
phase4_edges = [[2, 3], [6, 7], [18, 19], [22, 23]]
flag_phase4 = True
for arr in phase4_edges:
    tmp = [puzzle.Ep[i] for i in arr]
    if abs(tmp[0] - tmp[1]) != 1 or min(tmp) % 2:
        flag_phase4 = False
        break
if not flag_phase4 or [puzzle.Ce[i] for i in rl_center] != [2, 2, 2, 2, 4, 4, 4, 4] or [puzzle.Ce[i] for i in fb_center] != [1, 1, 1, 1, 3, 3, 3, 3] or [puzzle.Ce[i] for i in ud_center] != [0, 0, 0, 0, 5, 5, 5, 5]:
    for depth in range(len(ans) + 1, len(ans) + 10):
        if phase_4(puzzle, depth):
            break

print('phase 4',end=' ')
for i in ans:
    print(move_candidate[i], end=' ')
print('')
print('time:', time() - strt)
'''
'''
root = tkinter.Tk()
root.title("2x2x2solver")
root.geometry("400x300")

entry = [[None for _ in range(8)] for _ in range(6)]

dic = {'w':'white', 'g':'green', 'r':'red', 'b':'blue', 'o':'magenta', 'y':'yellow'}

for i in range(6):
    for j in range(8):
        if 1 < i < 4 or 1 < j < 4:
            canvas.create_rectangle(j * grid, i * grid, (j + 1) * grid, (i + 1) * grid, fill = 'gray')
            entry[i][j] = tkinter.Entry(width=2)
            entry[i][j].place(x = j * grid, y = i * grid)
'''


'''
cp = [1000 for _ in range(fac[8])]
co = [1000 for _ in range(3 ** 8)]
solved = Cube()
cp_idx, co_idx = solved.idx()
cp[cp_idx] = 0
co[co_idx] = 0
que = deque([[solved, 0, -10, -10, -10]])
while que:
    #print(len(que))
    status, num, l_mov_type, l2_mov_type, l3_mov_type = que.popleft()
    mov_cut = l_mov_type // 9 if l_mov_type // 9 == l2_mov_type // 9 == l3_mov_type // 9 else -10
    for mov in [0, 1, 2, 6, 7, 8, 9, 10, 11, 15, 16, 17, 18, 19, 20, 24, 25, 26]:
        if l_mov_type == mov // 3 or mov_cut == mov // 9:
            continue
        n_status = status.move(mov)
        cp_idx, co_idx = n_status.idx()
        flag = False
        if cp[cp_idx] == 1000:
            flag = True
            cp[cp_idx] = num + 1
        if co[co_idx] == 1000:
            flag = True
            co[co_idx] = num + 1
        if flag:
            que.append([n_status, num + 1, mov // 3, l_mov_type, l2_mov_type])
'''