from solver_c_31 import solver
#from cube_class_c_4 import move_candidate
from time import time
import urllib.request
import csv
import os

def main():
    global puzzle
    for num in range(100):
        
        response = urllib.request.urlopen('http://localhost:2014/scramble/.txt?e=444')
        scramble = response.read().decode('utf8', 'ignore').rstrip(os.linesep)
        print(scramble)
        inpt = [i for i in scramble.split()]
        #inpt = [i for i in input("scramble: ").split()]
        print(num)
        if inpt == []:
            exit()
        strt = time()
        solution = solver(inpt)
        print(solution)
        print(len(solution.split()), 'moves')
        print(time() - strt, 'sec')
        print('')

if __name__ == '__main__':
    main()