# -*- coding: utf-8 -*-
'''
4x4x4 Solver Main Part Written by Nyanyan
Copyright 2020 Nyanyan
'''

#from solver_c_1 import solver
from cube_class import face, wide, axis
from time import time, sleep
import tkinter
import cv2
import serial


def inspection_p():
    global solutionvar
    
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
    #solution = solver(state, [0.5, 5, 2, 2, 2, 3], 30)
    solution = [0, 12, 2, 14]
    robotize(solution, 300)
    solutionvar.set(str(len(solution)) + 'moves')

# Get colors of stickers
def detect():
    state = [-1 for _ in range(96)]
    capture = cv2.VideoCapture(0)
    for face in range(6):
        for mode in range(2):
            if mode == 0:
                tmp = 1
            else:
                tmp = 0
            move_actuator(0, tmp, 1000)
            move_actuator(1, tmp, 1000)
            sleep(1)
            move_actuator(0, (tmp + 1) % 2, 4000)
            move_actuator(1, (tmp + 1) % 2, 4000)
            #color: g, b, r, o, y, w
            # for normal sticker
            color_low = [[50, 50, 50],   [90, 50, 50],   [160, 140, 50], [160, 50, 50],  [20, 20, 50],   [0, 0, 50]]
            color_hgh = [[90, 255, 255], [140, 255, 255], [20, 255, 255], [20, 140, 255], [50, 255, 255], [179, 40, 255]]
            #color_low = [[40, 50, 50],   [90, 50, 50],   [160, 70, 50], [0, 20, 50],  [20, 50, 50],   [0, 0, 50]]
            #color_hgh = [[90, 255, 255], [140, 255, 255], [180, 255, 200], [20, 255, 255], [40, 255, 255], [179, 50, 255]]
            color_idx = [1, 3, 2, 4, 5, 0]
            circlecolor = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 170, 255), (0, 255, 255), (255, 255, 255)]
            d = 15
            size_x = 100
            size_y = 100
            center = [size_x // 2, size_y // 2]
            delta = [-3, -1, 1, 3]
            loopflag = [1 for _ in range(16)]
            mode_flag = [{0, 4, 5, 6, 7, 8, 9, 10, 11, 15}, {1, 2, 3, 12, 13, 14}]
            while sum([loopflag[i] for i in mode_flag[mode]]):
                ret, frame = capture.read()
                frame = cv2.resize(frame, (size_x, size_y))
                hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
                colors = [-1 for _ in range(16)]
                for y in range(4):
                    for x in range(4):
                        if not y * 4 + x in mode_flag[mode]:
                            continue
                        y_coord = center[1] + d * delta[y]
                        x_coord = center[0] + d * delta[x]
                        idx = face * 16 + y * 4 + x
                        cv2.circle(frame, (x_coord, y_coord), 2, (0, 0, 0), thickness=3, lineType=cv2.LINE_8, shift=0)
                        val = hsv[y_coord, x_coord]
                        for color in range(6):
                            for k in range(3):
                                if not ((color_low[color][k] < color_hgh[color][k] and color_low[color][k] <= val[k] <= color_hgh[color][k]) or (color_low[color][k] > color_hgh[color][k] and (color_low[color][k] <= val[k] or val[k] <= color_hgh[color][k]))):
                                    break
                            else:
                                cv2.circle(frame, (x_coord, y_coord), 5, circlecolor[color], thickness=2, lineType=cv2.LINE_8, shift=0)
                                cv2.circle(frame, (x_coord, y_coord), 10, (0, 0, 0), thickness=1, lineType=cv2.LINE_8, shift=0)
                                colors[y * 4 + x] = color_idx[color]
                cv2.imshow('frame', frame)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    for i in mode_flag[mode]:
                        idx = face * 16 + i
                        state[idx] = colors[i]
                    break
            print(face, mode, 'done')
            cv2.destroyAllWindows()
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

def release_arm():
    for i in range(2):
        for j in range(2):
            move_actuator(j, i, 4000)

def calibration():
    for i in range(2):
        for j in range(2):
            move_actuator(j, i, 90, 200)
        sleep(0.2)

def robotize(solution, rpm=300):
    global robot_solution
    for twist in solution:
        amount = (twist % 3 + 1) * 90
        wide_flag = wide(twist)
        axis_arr = [1, 3, 0, 2, 0, 2]
        move_arm = axis_arr[twist // 6]
        if axis(twist) == 1: # U or D
            robot_solution.append([0, 4000])
            robot_solution.append([2, 4000])
            robot_solution.append([1, -90, rpm])
            robot_solution.append([3, 90, rpm])
            robot_solution.append([0, 1000])
            robot_solution.append([1, 1000])
            robot_solution.append([2, 1000])
            robot_solution.append([3, 1000])
        grab_arms = [move_arm % 2, move_arm % 2 + 2]
        if wide_flag:
            for i in grab_arms:
                robot_solution.append([i, 2000])
        else:
            robot_solution.append([move_arm, 3000])
        release_arms = [(move_arm + 1) % 2, (move_arm + 1) % 2 + 2]
        for i in release_arms:
            robot_solution.append([i, 4000])
        robot_solution.append([move_arm, amount, rpm])
        robot_solution.append([move_arm, 1000])
        if wide_flag:
            robot_solution.append([(move_arm + 2) % 4, 1000])
        for i in release_arms:
            robot_solution.append([i, 1000])
        if axis(twist) == 1: # U or D
            robot_solution.append([0, 4000])
            robot_solution.append([2, 4000])
            robot_solution.append([1, 90, rpm])
            robot_solution.append([3, -90, rpm])
            robot_solution.append([0, 1000])
            robot_solution.append([2, 1000])

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
        '''
        if GPIO.input(21) == GPIO.LOW:
            if bluetoothmode:
                client_socket.send('emergency\n')
            solvingtimevar.set('emergency stop')
            print('emergency stop 1')
            return
        '''
        args = robot_solution[i]
        print(args)
        ser_num = args[0] // 2
        i += 1
        l = len(args)
        flag = False
        args_ad = robot_solution[i]
        if len(args_ad) == l and args_ad[0] % 2 == args[0] % 2:
            flag = True
            i += 1
        if l == 2: # command for arm
            move_actuator(ser_num, args[0] % 2, args[1])
            if flag:
                move_actuator((ser_num + 1) % 2, args_ad[0] % 2, args_ad[1])
            sleep(0.5)
        else:
            move_actuator(ser_num, args[0] % 2, args[1] + 5 * args[1] // abs(args[1]), args[2])
            if flag:
                move_actuator((ser_num + 1) % 2, args_ad[0] % 2, args_ad[1] + 5 * args_ad[1] // abs(args_ad[1]), args_ad[2])
            sleep(0.5)
            move_actuator(ser_num, args[0] % 2, -5 * args[1] // abs(args[1]), args[2])
            if flag:
                move_actuator((ser_num + 1) % 2, args_ad[0] % 2, -5 * args_ad[1] // abs(args_ad[1]), args_ad[2])
    solv_time = str(int((time() - strt_solv) * 1000) / 1000).ljust(5, '0')
    #solvingtimevar.set(solv_time + 's')
    print('solving time:', solv_time, 's')
    robot_solution = []


ser_motor = [None, None]
ser_motor[0] = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.01, write_timeout=0)
ser_motor[1] = serial.Serial('/dev/ttyUSB1', 9600, timeout=0.01, write_timeout=0)

sleep(5)


state = [-1 for _ in range(96)]
robot_solution = []

root = tkinter.Tk()
root.title("Solvour")
root.geometry("320x240")

grid = 10
offset_x = 50
offset_y = 20
entry = [[None for _ in range(16)] for _ in range(12)]
for i in range(12):
    for j in range(16):
        if 3 < i < 8 or 3 < j < 8:
            entry[i][j] = tkinter.Entry(master=root, bg='gray')
            entry[i][j].place(x = j * grid + offset_x, y = i * grid + offset_y, height=10, width=10)

inspection = tkinter.Button(root, text="inspection", command=inspection_p)
inspection.place(x=0, y=0)

solutionvar = tkinter.StringVar(master=root, value='aa')
solution = tkinter.Label(textvariable=solutionvar)
solution.place(x=210, y=50)

solvingtimevar = tkinter.StringVar(master=root, value='')
solvingtime = tkinter.Label(textvariable=solvingtimevar)
solvingtime.place(x=210, y=70)

grab = tkinter.Button(root, text="grab", command=grab_arm)
grab.place(x=0, y=150)

release = tkinter.Button(root, text="release", command=release_arm)
release.place(x=150, y=150)

calib = tkinter.Button(root, text='calibration', command=calibration)
calib.place(x=150, y=0)

start = tkinter.Button(root, text="start", command=start_p)
start.place(x=150, y=110)
root.mainloop()

for i in range(2):
    ser_motor[i].close()
