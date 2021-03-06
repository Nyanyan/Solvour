# -*- coding: utf-8 -*-
'''
4x4x4 Solver Main Part Written by Nyanyan
Copyright 2020 Nyanyan
'''

from solver_c_20 import solver
from time import time
import tkinter
import cv2


# パズルの状態の取得
# Get colors of stickers
def detect():
    global entry
    state = [-1 for _ in range(96)]
    capture = cv2.VideoCapture(2)
    for face in range(6):
        #color: g, b, r, o, y, w
        # for normal sticker
        color_low = [[50, 50, 50],   [90, 50, 50],   [160, 140, 50], [160, 50, 50],  [20, 20, 50],   [0, 0, 50]]
        color_hgh = [[90, 255, 255], [140, 255, 255], [20, 255, 255], [20, 140, 255], [50, 255, 255], [179, 40, 255]]
        #color_low = [[40, 50, 50],   [90, 50, 50],   [160, 70, 50], [0, 20, 50],  [20, 50, 50],   [0, 0, 50]]
        #color_hgh = [[90, 255, 255], [140, 255, 255], [180, 255, 200], [20, 255, 255], [40, 255, 255], [179, 50, 255]]
        color_idx = [1, 3, 2, 4, 5, 0]
        circlecolor = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 170, 255), (0, 255, 255), (255, 255, 255)]
        d = 25
        size_x = 400
        size_y = 300
        center = [size_x // 2, size_y // 2]
        delta = [-3, -1, 1, 3]
        loopflag = [1 for _ in range(16)]
        while sum(loopflag):
            ret, frame = capture.read()
            frame = cv2.resize(frame, (size_x, size_y))
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            for y in range(4):
                for x in range(4):
                    y_coord = center[1] + d * delta[y]
                    x_coord = center[0] + d * delta[x]
                    idx = face * 16 + y * 4 + x
                    cv2.circle(frame, (x_coord, y_coord), 5, (0, 0, 0), thickness=3, lineType=cv2.LINE_8, shift=0)
                    val = hsv[y_coord, x_coord]
                    for color in range(6):
                        flag = True
                        for k in range(3):
                            if not ((color_low[color][k] < color_hgh[color][k] and color_low[color][k] <= val[k] <= color_hgh[color][k]) or (color_low[color][k] > color_hgh[color][k] and (color_low[color][k] <= val[k] or val[k] <= color_hgh[color][k]))):
                                break
                        else:
                            cv2.circle(frame, (x_coord, y_coord), 15, circlecolor[color], thickness=3, lineType=cv2.LINE_8, shift=0)
                            cv2.circle(frame, (x_coord, y_coord), 20, (0, 0, 0), thickness=2, lineType=cv2.LINE_8, shift=0)
                            if cv2.waitKey() == 32:
                                state[idx] = color_idx[color]
                                loopflag[y * 4 + x] = 0
                                break
            cv2.imshow('frame', frame)
        print(face, 'done')
    capture.release()
    return state

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



state = [-1 for _ in range(96)]

root = tkinter.Tk()
root.title("Solvour")
root.geometry("500x300")

grid = 20
offset = 50

entry = [[None for _ in range(16)] for _ in range(12)]
for i in range(12):
    for j in range(16):
        if 3 < i < 8 or 3 < j < 8:
            entry[i][j] = tkinter.Entry(master=root, width=2, bg='gray')
            entry[i][j].place(x = j * grid + offset, y = i * grid + offset)


# scramble: L2 B L2 F' R2 F' D2 B D2 L D2 B2 D2 F2 D F R U L' Fw2 R U2 Rw2 F L2 F2 Rw2 B' R B' Rw2 Uw' R' U' Rw2 F' R' Fw' Uw' Fw' Rw2 B2 Rw U'
state = [
        0, 2, 2, 5, 2, 2, 3, 3, 4, 5, 1, 0, 1, 1, 5, 0, # D
        0, 2, 4, 2, 2, 1, 0, 5, 5, 2, 5, 5, 1, 0, 2, 4, # B
        2, 1, 3, 3, 1, 4, 0, 0, 0, 5, 4, 5, 1, 0, 0, 4, # U
        5, 2, 2, 1, 3, 0, 4, 1, 4, 1, 0, 4, 3, 5, 1, 2, # F
        0, 4, 4, 5, 5, 1, 2, 3, 1, 4, 3, 3, 3, 4, 3, 3, # R
        5, 0, 3, 4, 1, 3, 3, 4, 3, 2, 5, 0, 2, 1, 5, 4  # L
        ]

'''
state = [ # DP state
        5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 
        0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
        4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
        4, 4, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4
        ]
'''
'''
state = [ # OP state
        5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
        3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 
        1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4
        ]
'''
#state = detect()
fill_box(state)
print(state)
strt = time()
solution = solver(state, [0.5, 5, 2, 2, 2, 3], 30)
if solution == 'Error':
    print('failed')
else:
    print(solution)
    print(len(solution.split()), 'moves')
    print(time() - strt, 'sec')
    print('')

root.mainloop()