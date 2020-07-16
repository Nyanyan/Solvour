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




move_candidate = ["R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'"]

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
        pls = [[1, 2, 1, 2], [0, 0, 0, 0], [2, 1, 2, 1]]
        res = [i for i in self.Co]
        mov_type = mov // 3
        mov_amount = mov % 3
        for i in range(4):
            res[surface[mov_type][(i + mov_amount + 1) % 4]] = (self.Co[surface[mov_type][i]] + pls[mov_amount][i]) % 3
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
                   [[8, 9, 10, 11], [2, 12, 23, 6], [1, 15, 21, 5]], # Rw
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

cube = Cube()
