# -*- coding: utf-8 -*-
'''
4x4x4 Solver Test Part Written by Nyanyan
Copyright 2020 Nyanyan
'''

from solver_c_21 import solver
from cube_class import Cube, move_candidate
from time import time
import urllib.request
import csv
import os

def scramble_to_state(scramble):
    cube = Cube()
    for i in scramble:
        cube = cube.move(i)
    res = [-1 for _ in range(96)]
    corners = [[32, 80, 28], [35, 31, 67], [44, 48, 83], [47, 64, 51], [0, 95, 60], [3, 63, 76], [12, 16, 92], [15, 79, 19]]
    corner_colors = [[0, 4, 3], [0, 3, 2], [0, 1, 4], [0, 2, 1], [5, 4, 1], [5, 1, 2], [5, 3, 4], [5, 2, 3]]
    for i in range(8):
        cp = cube.Cp[i]
        co = cube.Co[i]
        for j, idx in enumerate(corners[i]):
            res[idx] = corner_colors[cp][(j - co) % 3]
    edges = [[33, 29], [30, 34], [39, 66], [65, 43], [46, 50], [49, 45], [40, 82], [81, 36], [87, 52], [56, 91], [72, 59], [55, 68], [71, 27], [23, 75], [88, 20], [24, 84], [1, 61], [62, 2], [7, 77], [78, 11], [14, 18], [17, 13], [8, 93], [94, 4]]
    edge_colors = [[0, 3], [3, 0], [0, 2], [2, 0], [0, 1], [1, 0], [0, 4], [4, 0], [4, 1], [1, 4], [2, 1], [1, 2], [2, 3], [3, 2], [4, 3], [3, 4], [5, 1], [1, 5], [5, 2], [2, 5], [5, 3], [3, 5], [5, 4], [4, 5]]
    for i in range(24):
        ep = cube.Ep[i]
        for j, idx in enumerate(edges[i]):
            res[idx] = edge_colors[ep][j]
    centers = [37, 38, 42, 41, 53, 54, 58, 57, 69, 70, 74, 73, 26, 25, 21, 22, 85, 86, 90, 89, 5, 6, 10, 9]
    for i in range(24):
        res[centers[i]] = cube.Ce[i]
    return res




state = [-1 for _ in range(96)]

for num in range(100):
    response = urllib.request.urlopen('http://localhost:2014/scramble/.txt?e=444')
    scramble = response.read().decode('utf8', 'ignore').rstrip(os.linesep)
    print(num)
    print(scramble)
    state = scramble_to_state([move_candidate.index(i) for i in scramble.split()])
    print(state)
    strt = time()
    solution = solver(state, [0.5, 5, 3, 3, 3, 5], 30)
    if solution == 'Error':
        print('failed')
    else:
        print(solution)
        l = len(solution.split())
        tim = time() - strt
        print(l, 'moves')
        print(tim, 'sec')
        print('')
        with open('analytics.csv', mode='a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow([tim, l])
