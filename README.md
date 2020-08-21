# Solvour

A 4x4x4 Rubik’s Cube Solving Robot

## About / 概要

Solvour is a 4x4x4 rubik’s cube solving robot. This robot is developed to break the world record of solving time of a 4x4x4 rubik’s cube by a robot.

Solvourは4x4x4ルービックキューブを解くロボットです。4x4x4ルービックキューブをロボットが解く時間において世界記録を更新することを目指して製作されたロボットです。

![Solvour1](https://github.com/Nyanyan/Solvour/blob/master/img/Solvour.jpg)

[![Soltvvo](http://img.youtube.com/vi/a2EKRblF6is/0.jpg)](https://youtu.be/a2EKRblF6is)



## Files and Directories / ファイルとディレクトリ

### 4x4x4solver

#### analytics.csv, analytics.xlsx

Analytics

統計

#### cube_class.py

The functions used widely

広く使われる関数群

#### main.py

Main program

メインプログラム

#### move_table.py

Generate tables of moving

パズルを動かすことに関する表の生成

#### prun_table.py

Generate tables of prunning

枝刈りに関する表の生成

#### setup_solver.py

Build Cython

Cythonのビルド

#### solver_c.py

C code built by Cython

Cythonビルドで生成されたCのコード

#### solver_c.pyx

Solver program

ソルバーのプログラム

#### solver_c_X.cp38-win_amd64.pyd

pyd file built by Cython

Cythonビルドで生成されたpydファイル

#### test.py

Program to test the code

テスト用コード

### Solvour1

#### main.py

Main Program for Solvour

Solvourのメインプログラム

#### Solvour1_arduino

Program for ATMEGA328P

ATMEGA328P用プログラム

#### Others

The same as 4x4x4solver

4x4x4solverと同じ