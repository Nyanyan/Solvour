# -*- coding: utf-8 -*-
'''
4x4x4 Solver Main Part Written by Nyanyan
Copyright 2020 Nyanyan
'''

#from solver_c_1 import solver
from cube_class import face
from time import time, sleep
import tkinter
import cv2
import serial


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

def grab_arm():
    for i in range(2):
        for j in range(2):
            move_actuator(j, i, 1000)
            sleep(1)

def robotize(solution, rpm):
    res = []
    for twist in solution:
        res.append([0, 1000])
        res.append([2, 1000])
        res.append([1, 1000])
        res.append([3, 1000])
        face_twist = face(twist)
        amount = (twist % 3 + 1) * 90
        if face_twist == 0:
            res.append([1, 3000])
            res.append([3, 1000])
            res.append([0, 4000])
            res.append([2, 4000])
            res.append([1, amount, rpm])
        elif face_twist == 1:
            res.append([1, 2000])
            res.append([3, 2000])
            res.append([0, 4000])
            res.append([2, 4000])
            res.append([1, amount, rpm])
        elif face_twist == 2:
            res.append([1, 1000])
            res.append([3, 3000])
            res.append([0, 4000])
            res.append([2, 4000])
            res.append([3, amount, rpm])
        elif face_twist == 4:
            res.append([0, 4000])
            res.append([2, 4000])
            res.append([1, 270, rpm])
            res.append([3, 90, rpm])
            res.append([0, 1000])
            res.append([1, 1000])
            res.append([2, 1000])
            res.append([3, 1000])

            res.append([0, 3000])
            res.append([2, 1000])
            res.append([1, 4000])
            res.append([3, 4000])
            res.append([0, amount, rpm])

            res.append([0, 1000])
            res.append([1, 1000])
            res.append([2, 1000])
            res.append([3, 1000])
            res.append([0, 4000])
            res.append([2, 4000])
            res.append([1, 90, rpm])
            res.append([3, 270, rpm])
        elif face_twist == 5:
            res.append([0, 4000])
            res.append([2, 4000])
            res.append([1, 270, rpm])
            res.append([3, 90, rpm])
            res.append([0, 1000])
            res.append([1, 1000])
            res.append([2, 1000])
            res.append([3, 1000])

            res.append([0, 2000])
            res.append([2, 2000])
            res.append([1, 4000])
            res.append([3, 4000])
            res.append([0, amount, rpm])

            res.append([0, 1000])
            res.append([1, 1000])
            res.append([2, 1000])
            res.append([3, 1000])
            res.append([0, 4000])
            res.append([2, 4000])
            res.append([1, 90, rpm])
            res.append([3, 270, rpm])
        elif face_twist == 6:
            res.append([0, 4000])
            res.append([2, 4000])
            res.append([1, 270, rpm])
            res.append([3, 90, rpm])
            res.append([0, 1000])
            res.append([1, 1000])
            res.append([2, 1000])
            res.append([3, 1000])

            res.append([0, 1000])
            res.append([2, 3000])
            res.append([1, 4000])
            res.append([3, 4000])
            res.append([2, amount, rpm])

            res.append([0, 1000])
            res.append([1, 1000])
            res.append([2, 1000])
            res.append([3, 1000])
            res.append([0, 4000])
            res.append([2, 4000])
            res.append([1, 90, rpm])
            res.append([3, 270, rpm])
        elif face_twist == 8:
            res.append([0, 3000])
            res.append([2, 1000])
            res.append([1, 4000])
            res.append([3, 4000])
            res.append([0, amount, rpm])
        elif face_twist == 9:
            res.append([0, 2000])
            res.append([2, 2000])
            res.append([1, 4000])
            res.append([3, 4000])
            res.append([0, amount, rpm])
        elif face_twist == 8:
            res.append([0, 1000])
            res.append([2, 3000])
            res.append([1, 4000])
            res.append([3, 4000])
            res.append([2, amount, rpm])
    return res

# Send commands to move actuators
def move_actuator(num, arg1, arg2, arg3=None):
    if arg3 == None:
        com = str(arg1) + ' ' + str(arg2)
    else:
        com = str(arg1) + ' ' + str(arg2) + ' ' + str(arg3)
    if ser_motor[num].in_waiting:
        ser_motor[num].reset_output_buffer()
    ser_motor[num].write((com + '\n').encode())
    ser_motor[num].flush()

# Move robot
def start_p():
    global robot_solution
    print('start!')
    strt_solv = time()
    i = 0
    while i < len(robot_solution):
        args = robot_solution[i]
        ser_num = args[0] // 2
        arg1 = args[0] % 2
        if len(args) == 2: # command for arm
            move_actuator(ser_num, arg1, args[1])
        else:
            move_actuator(ser_num, arg1, args[1], args[2])
        sleep(1)
        '''
        if GPIO.input(21) == GPIO.LOW:
            if bluetoothmode:
                client_socket.send('emergency\n')
            solvingtimevar.set('emergency stop')
            print('emergency stop 1')
            return
        
        if i != 0:
            grab = ans[i][0] % 2
            for j in range(2):
                move_actuator(j, grab, 1000)
            sleep(slp1)
            for j in range(2):
                move_actuator(j, (grab + 1) % 2, 2000)
            sleep(slp2)
        ser_num = ans[i][0] // 2
        offset = 0
        before = ser_motor[ans[i][0] // 2].in_waiting
        move_actuator(ser_num, ans[i][0] % 2, ans[i][1] * 90 + offset, rpm)
        max_turn = abs(ans[i][1])
        flag = i < len(ans) - 1 and ans[i + 1][0] % 2 == ans[i][0] % 2
        if flag:
            before2 = ser_motor[ans[i + 1][0] // 2].in_waiting
            move_actuator(ans[i + 1][0] // 2, ans[i + 1][0] % 2, ans[i + 1][1] * 90 + offset, rpm)
            max_turn = max(max_turn, abs(ans[i + 1][1]))
        slptim = 2 * 60 / rpm * (max_turn * 90 - offset) / 360 * ratio
        sleep(slptim)
        i += 1 + int(flag)
        '''
    solv_time = str(int((time() - strt_solv) * 1000) / 1000).ljust(5, '0')
    #solvingtimevar.set(solv_time + 's')
    print('solving time:', solv_time, 's')
    robot_solution = []

'''
ser_motor = [None, None]
ser_motor[0] = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.01, write_timeout=0)
ser_motor[1] = serial.Serial('/dev/ttyUSB1', 9600, timeout=0.01, write_timeout=0)
'''

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
#solution = solver(state, [0.5, 5, 2, 2, 2, 3], 30)
solution = [0, 12]
if solution == 'Error':
    print('failed')
    exit()
robot_solution = robotize(solution, 300)
print(robot_solution)
print(solution)
print(len(solution), 'moves')
print(time() - strt, 'sec')
print('')
grab_arm()
sleep(5)
start_p()

root.mainloop()