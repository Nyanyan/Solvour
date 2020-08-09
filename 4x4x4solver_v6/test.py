# -*- coding: utf-8 -*-
'''
4x4x4 Solver Test Part Written by Nyanyan
Copyright 2020 Nyanyan
'''

from solver_c_14 import solver
from cube_class import Cube
from time import time
import urllib.request
import csv
import os


def fill_box(state):
    global entry
    strt = [[8, 4], [4, 12], [0, 4], [4, 4], [4, 8], [4, 0]]
    colors = ['white', 'green', 'red', 'blue', 'magenta', 'yellow']
    for face in range(6):
        tmp_arr = [i for i in state[face * 16:(face + 1) * 16]]
        if face == 1:
            tmp_arr = list(reversed(tmp_arr))
        for y in range(4):
            for x in range(4):
                y_coord = strt[face][0] + y
                x_coord = strt[face][1] + x
                entry[y_coord][x_coord]['bg'] = colors[tmp_arr[y * 4 + x]]

def scramble_to_state(scramble):
    cube = Cube()
    for i in scramble:
        cube = cube.move(i)
    corners = [[32, 80, 28], [35, 31, 67], [44, 48, 83], [47, 64, 51], [0, 95, 60], [3, 63, 76], [12, 16, 92], [15, 79, 19]]
    corners = [[0, 4, 3], [0, 3, 2], [0, 1, 4], [0, 2, 1], [5, 4, 1], [5, 1, 2], [5, 3, 4], [5, 2, 3]]




state = [-1 for _ in range(96)]

grid = 20
offset = 50
entry = [[None for _ in range(16)] for _ in range(12)]
for i in range(12):
    for j in range(16):
        if 3 < i < 8 or 3 < j < 8:
            entry[i][j] = tkinter.Entry(master=root, width=2, bg='gray')
            entry[i][j].place(x = j * grid + offset, y = i * grid + offset)

for _ in range(100):
    response = urllib.request.urlopen('http://localhost:2014/scramble/.txt?e=444')
    scramble = response.read().decode('utf8', 'ignore').rstrip(os.linesep)

    fill_box(state)
    print(state)
    strt = time()
    solution = solver(state, [0.5, 5, 2, 2, 2, 3], 30)
    if solution == 'Error':
        print('failed')
    else:
        print(solution)
        l = len(solution.split())
        tim = time() - strt
        print(l, 'moves')
        print(tim, 'sec')
        with open('analytics.csv', mode='a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow([tim, l])

    root.mainloop()