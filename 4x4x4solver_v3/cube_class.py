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

fac = [1 for _ in range(25)]
for i in range(1, 25):
    fac[i] = fac[i - 1] * i

def cmb(n, r):
    return fac[n] // fac[r] // fac[n - r]

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

    def idx_cp(self):
        res = 0
        for i in range(8):
            cnt = self.Cp[i]
            for j in self.Cp[:i]:
                if j < self.Cp[i]:
                    cnt -= 1
            res += fac[7 - i] * cnt
        return res
    
    def idx_co(self):
        res = 0
        for i in range(7):
            res *= 3
            res += self.Co[i]
        return res

    def idx_ce_phase0(self):
        res = 0
        cnt = 0
        for i in range(23):
            if self.Ce[i] == 2 or self.Ce[i] == 4:
                res += cmb(23 - i, 8 - cnt)
                cnt += 1
                if cnt == 8 or i - cnt == 15:
                    break
        return res

    def idx_ce_phase1_fbud(self):
        res = 0
        cnt = 0
        arr = [0, 1, 2, 3, 20, 21, 22, 23, 4, 5, 6, 7, 12, 13, 14, 15] # FBUD centers
        for i in range(15):
            if self.Ce[arr[i]] == 1 or self.Ce[arr[i]] == 3:
                res += cmb(15 - i, 8 - cnt)
                cnt += 1
                if cnt == 8 or i - cnt == 7:
                    break
        return res
    
    def idx_ce_phase1_rl(self):
        res = 0
        cnt = 0
        for i in range(7): # RL centers
            if self.Ce[rl_center[i]] == 4:
                res += cmb(7 - i, 4 - cnt)
                cnt += 1
                if cnt == 4 or i - cnt == 3:
                    break
        return res
    
    def idx_high_low_edge(self):
        arr = [int(self.Ep[i] % 2 != i % 2) for i in range(24)]
        parts = [[0, 1, 4, 5, 16, 17, 20, 21], [6, 7, 2, 3, 18, 19, 22, 23], [9, 8, 11, 10, 13, 12, 15, 14]] #MSE

        res = []
        for m_parts in parts:
            tmp = 0
            for i in range(8):
                tmp *= 2
                tmp += arr[m_parts[i]]
            res.append(tmp)
        res = res[0] * 65536 + res[1] * 256 + res[2]
        return res
    
    def ce_parity(self):
        arr = [[8, 11], [9, 10], [16, 19], [17, 18]]
        for m_arr in arr:
            if self.Ce[m_arr[0]] != self.Ce[m_arr[1]]:
                return 1
        return 0

def face(twist):
    return twist // 3

def axis(twist):
    return twist // 12

def wide(twist):
    return (twist // 3) % 2

'''
def move_idx_high_low_edge(num, twist):
    edge = [(num >> i) & 1 for i in reversed(range(23))]
    if sum(edge) % 2:
        edge.append(1)
    else:
        edge.append(0)
    #print('bef', edge)
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
    mov_type = twist // 3
    mov_amount = twist % 3
    prd = [i for i in edge]
    for idx, arr in enumerate(surface[mov_type]):
        for i in range(4):
            prd[arr[(i + mov_amount + 1) % 4]] = edge[arr[i]]
            if mov_amount != 1 and (idx > 1 or mov_type < 4):
                prd[arr[(i + mov_amount + 1) % 4]] += 1
                prd[arr[(i + mov_amount + 1) % 4]] %= 2
    #print('prd', prd)
    res = 0
    for i in range(23):
        res *= 2
        res += prd[i]
    return res
'''
rl_center = [8, 9, 10, 11, 16, 17, 18, 19]
fb_center = [4, 5, 6, 7, 12, 13, 14, 15]
ud_center = [0, 1, 2, 3, 20, 21, 22, 23]