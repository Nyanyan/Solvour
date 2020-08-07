'''
4x4x4 Solver Main Part Written by Nyanyan
Copyright 2020 Nyanyan
'''

from solver_c_3 import solver
from time import time
'''
import urllib.request
import csv
import os
'''

def main():
    global puzzle
    for num in range(1):
        # scramble: L2 B L2 F' R2 F' D2 B D2 L D2 B2 D2 F2 D F R U L' Fw2 R U2 Rw2 F L2 F2 Rw2 B' R B' Rw2 Uw' R' U' Rw2 F' R' Fw' Uw' Fw' Rw2 B2 Rw U'
        state = [
                0, 2, 2, 5, 2, 2, 3, 3, 4, 5, 1, 0, 1, 1, 5, 0, # D
                0, 2, 4, 2, 2, 1, 0, 5, 5, 2, 5, 5, 1, 0, 2, 4, # B
                2, 1, 3, 3, 1, 4, 0, 0, 0, 5, 4, 5, 1, 0, 0, 4, # U
                5, 2, 2, 1, 3, 0, 4, 1, 4, 1, 0, 4, 3, 5, 1, 2, # F
                0, 4, 4, 5, 5, 1, 2, 3, 1, 4, 3, 3, 3, 4, 3, 3, # R
                5, 0, 3, 4, 1, 3, 3, 4, 3, 2, 5, 0, 2, 1, 5, 4  # L
                ]
        #response = urllib.request.urlopen('http://localhost:2014/scramble/.txt?e=444')
        #scramble = response.read().decode('utf8', 'ignore').rstrip(os.linesep)
        #print(num)
        #print(scramble)
        #inpt = [i for i in scramble.split()]
        #inpt = [i for i in input("scramble: ").split()]
        strt = time()
        solution = solver(state)
        if solution == -1:
            print('failed')
            continue
        print(solution)
        print(len(solution.split()), 'moves')
        print(time() - strt, 'sec')
        print('')

if __name__ == '__main__':
    main()