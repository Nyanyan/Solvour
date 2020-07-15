move_candidate = ["R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'"]

class Cube:
    def __init__(self):
        self.Co = [0 for _ in range(8)]
        self.Cp = [i for i in range(8)]
        self.Eo = [0 for _ in range(24)]
        self.Ep = [i for i in range(24)]
        self.Ce = [i // 4 for i in range(24)]
    
    def move_cp(self, mov):
        surface = [[3, 1, 7, 5], [3, 1, 7, 5], [0, 2, 4, 6], [0, 1, 3, 2], [0, 1, 3, 2], [4, 5, 7, 6], [2, 3, 5, 4], [2, 3, 5, 4], [1, 0, 6, 7]]
        res = [i for i in self.Cp]
        mov_type = mov // 3
        mov_amount = mov % 3
        for i in range(4):
            res[surface[mov_type][(i + mov_amount) % 4]] = self.Cp[surface[mov_type][i]]
        return res
    
    def move_co(self, mov):
        surface = [[3, 1, 7, 5], [3, 1, 7, 5], [0, 2, 4, 6], [0, 1, 3, 2], [0, 1, 3, 2], [4, 5, 7, 6], [2, 3, 5, 4], [2, 3, 5, 4], [1, 0, 6, 7]]
        pls = [[2, 1, 1, 2], [0, 0, 0, 0], [1, 2, 2, 1]]
        res = [i for i in self.Co]
        mov_type = mov // 3
        mov_amount = mov % 3
        for i in range(4):
            res[surface[mov_type][(i + mov_amount) % 4]] = (self.Co[surface[mov_type][i]] + pls[mov_amount][i]) % 3
        return res
    
    def move_ep(self, mov):
        surface = []
