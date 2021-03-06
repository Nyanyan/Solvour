# -*- coding: utf-8 -*-
'''
Solvour Main Part Written by Nyanyan
Copyright 2020 Nyanyan
'''

#from solver_c_1 import solver
from cube_class import face, wide, axis
from time import time, sleep
import tkinter
import cv2
import serial
import RPi.GPIO as GPIO
import bluetooth
import subprocess


def inspection_p():
    global solutionvar, robot_solution
    
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
    if bluetoothmode:
        #state = detect()
        fill_box(state)
        send_state = ' '.join([str(i) for i in state])
        client_socket.send(send_state + '\n')
        solution = client_socket.recv(1024).decode('utf-8', 'ignore').replace('\n', '')
        solution = [int(i) for i in solution]
    else:
        #state = detect()
        fill_box(state)
        #                   0    1     2     3     4      5      6    7     8     9     10     11     12   13    14    15    16     17     18   19   20     21    22     23     24   25    26    27    28     29     30   31    32    33    34     35
        move_candidate = ["R", "R2", "R'", "Rw", "Rw2", "Rw'", "L", "L2", "L'", "Lw", "Lw2", "Lw'", "U", "U2", "U'", "Uw", "Uw2", "Uw'", "D", "D2", "D'", "Dw", "Dw2", "Dw'", "F", "F2", "F'", "Fw", "Fw2", "Fw'", "B", "B2", "B'", "Bw", "Bw2", "Bw'"]
        #solution = solver(state, [0.5, 5, 2, 2, 2, 3], 30)
        # R U Fw L2 F2 B Uw2 Rw' R F'
        # reverse: F R' Rw Uw2 B' F2 L2 Fw' U' R'
        #solution = [0, 12, 27, 7, 25, 30, 16, 5, 0, 26]
        # Rw2 Fw D' Fw L' R Uw L2 F2 Rw
        # reverse Rw' F2 L2 Uw' R' L Fw' D Fw' Rw2
        #solution = [4, 27, 20, 27, 8, 0, 15, 7, 25, 3]
        # Rw2 Fw D' Fw B' R Uw L2 F2 Rw R U Fw L2 F2 B Uw2 Rw' R F'
        # rev F R' Rw Uw2 B' F2 L2 Fw' U' R' Rw' F2 L2 Uw' R' B Fw' D Fw' Rw2
        #solution = [4, 27, 20, 27, 32, 0, 15, 7, 25, 3, 0, 12, 27, 7, 25, 30, 16, 5, 0, 26]
        # Fw B' R Uw L2 F2 Rw R U Fw
        # rev Fw' U' R' Rw' F2 L2 Uw' R' B Fw'
        solution = [27, 32, 0, 15, 7, 25, 3, 0, 12, 27]
        # R U R' U'
        #solution = [0, 12, 2, 14]
        '''
        state_reshape = [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16]
        face_coord = ['U', 'F', 'R', 'B', 'L', 'D']
        state_str = ''.join([face_coord[state[i]] for i in state_reshape])
        solution_str = subprocess.check_output(['java', '-cp', '.:threephase.jar:twophase.jar', 'solver', state_str]).decode('utf-8', 'ignore')
        print(solution_str)
        solution = []
        for i in solution_str.split():
            print(i)
            if i in move_candidate:
                solution.append(move_candidate.index(i))
        print(solution)
        '''
    robot_solution = robotize(solution, 500)
    print(robot_solution)
    robot_solution = optimise(robot_solution)
    print(robot_solution)
    solutionvar.set(str(len(solution)) + 'moves')

# Get colors of stickers
def detect():
    rpm = 150
    commands = [
        [[1, 1000, 4000], [3, 1000, 4000], [0, 4000, 1000], [2, 4000, 1000], [1, 90, rpm], [3, -90, rpm]],
        [[1, 1000, 4000], [3, 1000, 4000], [0, 4000, 1000], [2, 4000, 1000], [1, 90, rpm], [3, -90, rpm]],
        [[1, 1000, 4000], [3, 1000, 4000], [0, 4000, 1000], [2, 4000, 1000], [1, 90, rpm], [3, -90, rpm]],
        [[0, 1000, 4000], [2, 1000, 4000], [1, 4000, 1000], [3, 4000, 1000], [0, 90, rpm], [2, -90, rpm]],
        [[0, 1000, 4000], [2, 1000, 4000], [1, 4000, 1000], [3, 4000, 1000], [0, 180, rpm], [2, -180, rpm]],
        [[0, 1000, 4000], [2, 1000, 4000], [1, 4000, 1000], [3, 4000, 1000], [0, 90, rpm], [2, -90, rpm], [1, 1000, 4000], [3, 1000, 4000], [0, 4000, 1000], [2, 4000, 1000], [1, 90, rpm], [3, -90, rpm]],
    ]
    state = [-1 for _ in range(96)]
    capture = cv2.VideoCapture(0)
    for face in range(6):
        for mode in range(2):
            coms = [[mode, 1000, 4000], [mode + 2, 1000, 4000], [(mode + 1) % 2, 4000, 1000], [(mode + 1) % 2 + 2, 4000, 1000]]
            move_commands(coms, 0.5, 0.5)
            #color: g, b, r, o, y, w
            # for normal sticker
            color_low = [[50, 50, 50],   [90, 50, 50],   [160, 170, 50], [160, 50, 50],  [20, 0, 20],   [0, 0, 50]]
            color_hgh = [[90, 255, 255], [140, 255, 255], [20, 255, 255], [20, 170, 255], [50, 255, 255], [179, 40, 255]]
            #color_low = [[40, 50, 50],   [90, 50, 50],   [160, 70, 50], [0, 20, 50],  [20, 50, 50],   [0, 0, 50]]
            #color_hgh = [[90, 255, 255], [140, 255, 255], [180, 255, 200], [20, 255, 255], [40, 255, 255], [179, 50, 255]]
            color_idx = [1, 3, 2, 4, 5, 0]
            circlecolor = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 170, 255), (0, 255, 255), (255, 255, 255)]
            dx = [-40, -5, 5, 40]
            dy = [-45, -11, 11, 45]
            d = [-3, 0, 3]
            size_x = 100
            size_y = 100
            center = [size_x // 2, size_y // 2]
            loopflag = [1 for _ in range(16)]
            mode_flag = [{1, 2, 3, 12, 13, 14}, {0, 4, 5, 6, 7, 8, 9, 10, 11, 15}]
            while sum([loopflag[i] for i in mode_flag[mode]]):
                ret, frame = capture.read()
                frame = cv2.resize(frame, (size_x, size_y))
                hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
                colors = [-1 for _ in range(16)]
                for y in range(4):
                    for x in range(4):
                        if not y * 4 + x in mode_flag[mode]:
                            continue
                        y_coord = center[1] + dy[y]
                        x_coord = center[0] + dx[x]
                        idx = face * 16 + y * 4 + x
                        cv2.circle(frame, (x_coord, y_coord), 2, (0, 0, 0), thickness=3, lineType=cv2.LINE_8, shift=0)
                        vals = [hsv[y_coord + d[i], x_coord + d[j]] for i in range(3) for j in range(3)]
                        vals.sort(key=lambda x: x[2])
                        val = vals[4]
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
        move_commands(commands[face], 0.5, 0.5)
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
            premove_1(j * 2 + i, 50)
            move_actuator([j * 2 + i, 1000])
            sleep(0.3)
            premove_2(j * 2 + i, 50)
            sleep(1)

def release_arm():
    for i in range(4):
            move_actuator([i, 4000])

def calibration():
    release_arm()
    sleep(0.5)
    for i in range(2):
        for j in range(2):
            #move_actuator([j * 2 + (i + 1) % 2, 45, 200])
            #sleep(0.1)
            move_actuator([j * 2 + i, 45, 300])
        sleep(0.07)
    for i in range(2):
        for j in range(2):
            #move_actuator([j * 2 + (i + 1) % 2, 45, 200])
            #sleep(0.1)
            move_actuator([j * 2 + i, 0, 300])
        sleep(0.14)

def robotize(solution, rpm=200):
    regrip_rpm = 250
    robot_solution = []
    for twist in solution:
        amount = (twist % 3 + 1) * 90
        wide_flag = wide(twist)
        axis_arr = [1, 3, 0, 2, 0, 2]
        move_arm = axis_arr[twist // 6]
        if axis(twist) == 1: # U or D
            robot_solution.append([0, 4000])
            robot_solution.append([2, 4000])
            robot_solution.append([3, 90, regrip_rpm])
            robot_solution.append([1, -90, regrip_rpm])
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
            robot_solution.append([1, 90, regrip_rpm])
            robot_solution.append([3, -90, regrip_rpm])
            robot_solution.append([0, 1000])
            robot_solution.append([2, 1000])
    return robot_solution

def optimise(robot_solution):
    res = []
    arms = [1000 for _ in range(4)]
    pre_arms = [1000 for _ in range(4)]
    for command in robot_solution:
        if command[1] < 1000:
            res.append(command)
            #print(command)
            continue

        if arms[command[0]] < command[1] < 2000: # MODIFIED
            for i in reversed(range(len(res))):
                if res[i][0] == command[0] and res[i][1] >= 1000:
                    del res[i]
                    command.append(pre_arms[command[0]])
                    res.append(command)
                    arms[command[0]] = command[1]
                    break
                elif res[i][1] < 1000 or res[i][0] % 2 != command[0] % 2:
                    command.append(arms[command[0]])
                    res.append(command)
                    pre_arms[command[0]] = arms[command[0]]
                    arms[command[0]] = command[1]
                    break
            else:
                command.append(pre_arms[command[0]])
                res.append(command)
                arms[command[0]] = command[1]
            continue

        if pre_arms[command[0]] == command[1] == 4000:
            for i in reversed(range(len(res))):
                if res[i][1] < 1000:
                    break
                if res[i][0] % 2 != command[0] % 2:
                    break
                if res[i][0] == command[0]:
                    arms[command[0]] = pre_arms[command[0]]
                    del res[i]
                    continue
        if arms[command[0]] == command[1]:
            continue
        command.append(arms[command[0]])
        res.append(command)
        pre_arms[command[0]] = arms[command[0]]
        arms[command[0]] = command[1]
        #print(arms)
        #print(arms)
    i = len(res) - 1
    while i > 0:
        if res[i][1] < 1000:
            if res[i - 1][1] < 1000 and res[i][1] + res[i - 1][1] == 0:
                for _ in range(2):
                    del res[-1]
                i -= 2
            else:
                break
        else:
            del res[i]
            i -= 1
    return res

def premove_1(arm, rpm):
    premove = []
    amount = 5
    if arm == 0:
        premove.append([1, amount, rpm])
        #premove.append([3, -amount, rpm])
    elif arm == 1:
        #premove.append([0, -amount, rpm])
        premove.append([2, amount, rpm])
    elif arm == 2:
        #premove.append([1, -amount, rpm])
        premove.append([3, amount, rpm])
    elif arm == 3:
        premove.append([0, amount, rpm])
        #premove.append([2, -amount, rpm])
    for twist in premove:
        move_actuator(twist)

def premove_2(arm, rpm):
    premove = []
    amount = 5
    if arm == 0:
        premove.append([1, -amount, rpm])
        #premove.append([3, amount, rpm])
    elif arm == 1:
        #premove.append([0, amount, rpm])
        premove.append([2, -amount, rpm])
    elif arm == 2:
        #premove.append([1, amount, rpm])
        premove.append([3, -amount, rpm])
    elif arm == 3:
        premove.append([0, -amount, rpm])
        #premove.append([2, amount, rpm])
    for twist in premove:
        move_actuator(twist)

# Send commands to move actuators
def move_actuator(arr):
    num = arr[0] // 2
    if len(arr) == 2:
        com = str(arr[0] % 2) + ' ' + str(arr[1])
    else:
        com = str(arr[0] % 2) + ' ' + str(arr[1]) + ' ' + str(arr[2])
    ser_motor[num].write((com + '\n').encode())

def move_commands(commands, arm_slp, ratio):
    i = 0
    strt = -1
    while i < len(commands):
        if GPIO.input(4) == GPIO.LOW:
            '''
            if bluetoothmode:
                client_socket.send('emergency\n')
            '''
            release_arm()
            solvingtimevar.set('emergency stop')
            print('emergency stop')
            return -1
        args = commands[i]
        i += 1
        if i < len(commands):
            args_ad = commands[i]
        type_same = (args[1] >= 1000 and args_ad[1] >= 1000) or (args[1] < 1000 and args_ad[1] < 1000)
        if args[2] >= 1000: # command for arm
            rpm = 150
            move_actuator(args[:2])
            max_d = abs(args[1] - args[2]) // 1000
            if args[1] < args[2] == 4000:
                premove_1(args[0], rpm)
            elif type_same and args_ad[0] % 2 == args[0] % 2:
                move_actuator(args_ad[:2])
                max_d = max(max_d, abs(args_ad[1] - args_ad[2]) // 1000)
                i += 1
            sleep(max_d * arm_slp)
            if args[1] < args[2] == 4000:
                premove_2(args[0], rpm)
        else:
            if strt == -1:
                strt = time()
            max_turn = abs(args[1])
            if type_same and args_ad[0] % 2 == args[0] % 2:
                move_actuator(args_ad)
                move_actuator(args)
                i += 1
                max_turn = max(max_turn, abs(args_ad[1]))
            else:
                args_adjust = [(args[0] + 1) % 2 + 2 * (1 - args[0] // 2), 0, args[2]]
                move_actuator(args)
                move_actuator(args_adjust)
            slptim = 2 * 60 / args[2] * max_turn / 360 * ratio
            sleep(slptim)
    return time() - strt

def start_p():
    global robot_solution
    print('start!')
    strt_solv = time()
    #move_commands(robot_solution, 0.09, 0.22)
    solv_time = str(int(move_commands(robot_solution, 0.09, 0.25) * 1000) / 1000).ljust(5, '0')
    #solv_time = str(int((time() - strt_solv) * 1000) / 1000).ljust(5, '0')
    solvingtimevar.set(solv_time + 's')
    print('solving time:', solv_time, 's')
    robot_solution = []
    sleep(0.5)
    release_arm()

ser_motor = [None, None]
ser_motor[0] = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01, write_timeout=0)
ser_motor[1] = serial.Serial('/dev/ttyUSB1', 115200, timeout=0.01, write_timeout=0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

bluetoothmode = False
if bluetoothmode:
    subprocess.call(['sh', 'bluetooth_script.sh'])
    PORT = 1
    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    print("connect...")
    server_socket.bind( ("",PORT ))
    server_socket.listen(1)
    client_socket,address = server_socket.accept()
    print("connection success!!")

sleep(1)

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

solutionvar = tkinter.StringVar(master=root, value='solution')
solution = tkinter.Label(textvariable=solutionvar)
solution.place(x=210, y=50)

solvingtimevar = tkinter.StringVar(master=root, value='time')
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
