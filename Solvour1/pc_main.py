import serial
from solver_c_1 import solver

def solve():
    receive = ser.readline().decode('utf-8','ignore').replace('\n', '')
    receive = [int(i) for i in receive]
    if len(receive) == 96:
        solution = solver(receive, [0.5, 5, 2, 2, 2, 3], 30)
        ser.write(solution.encode())

ser = serial.Serial('COM15', 9600, timeout=0.01, write_timeout=0)

while True:
    solve()