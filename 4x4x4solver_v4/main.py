from solver_c_22 import solver
from cube_class_c_4 import move_candidate, Cube
from time import time
import urllib.request
import csv
import os

def main():
    global puzzle
    for num in range(100):
        
        response = urllib.request.urlopen('http://localhost:2014/scramble/.txt?e=444')
        scramble = response.read().decode('utf8', 'ignore').rstrip(os.linesep)
        inpt = [i for i in scramble.split()]
        
        #inpt = [i for i in input("scramble: ").split()]
        print(num)
        if inpt == []:
            exit()
        scramble = [move_candidate.index(i) for i in inpt]
        puzzle = Cube()
        for mov in scramble:
            puzzle = puzzle.move(mov)
        strt = time()
        solution = solver(puzzle)
        if solution == [-1]:
            continue
        print('solution:',end=' ')
        #print(solution)
        for i in solution:
            print(move_candidate[i],end=' ')
        print('')
        print(len(solution), 'moves')
        print(time() - strt, 'sec')
        print('')

if __name__ == '__main__':
    main()