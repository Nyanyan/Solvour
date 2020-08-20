#include <Servo.h>

const int magnet_threshold = 30;
const long turn_steps = 400;
const int step_dir[2] = {11, 9};
const int step_pul[2] = {12, 10};
const int sensor[2] = {14, 15};
const int deg[2][4] = {{82, 97, 120, 160}, {77, 90, 110, 150}}; //2, 3
//const int deg[2][4] = {{85, 105, 120, 160}, {88, 105, 120, 160}}; //0, 1

char buf[30];
int idx = 0;
long data[3];

Servo servo0;
Servo servo1;

void move_motor(long num, long deg, long spd) {
  bool hl = true;
  if (deg < 0) hl = false;
  digitalWrite(step_dir[num], hl);
  long steps = abs(deg) * turn_steps / 360;
  long avg_time = 1000000 * 60 / turn_steps / spd;
  long max_time = 800;
  long slope = 100;
  bool motor_hl = false;
  long accel = min(steps / 2, max(0, (max_time - avg_time) / slope));
  int num1 = (num + 1) % 2;
  digitalWrite(step_dir[num1], HIGH);
  bool flag = (deg >= 90);
  for (int i = 0; i < accel; i++) {
    motor_hl = !motor_hl;
    digitalWrite(step_pul[num], motor_hl);
    //Serial.println(analogRead(sensor[0]));
    if (flag) {
      if (analogRead(sensor[num1]) > magnet_threshold)
        digitalWrite(step_pul[num1], motor_hl);
    }
    delayMicroseconds(max_time - slope * i);
  }
  for (int i = 0; i < steps * 2 - accel * 2; i++) {
    motor_hl = !motor_hl;
    digitalWrite(step_pul[num], motor_hl);
    //Serial.println(analogRead(sensor[0]));
    if (flag) {
      if (analogRead(sensor[num1]) > magnet_threshold)
        digitalWrite(step_pul[num1], motor_hl);
    }
    delayMicroseconds(avg_time);
  }
  for (int i = 0; i < accel; i++) {
    motor_hl = !motor_hl;
    digitalWrite(step_pul[num], motor_hl);
    //Serial.println(analogRead(sensor[0]));
    if (flag) {
      if (analogRead(sensor[num1]) > magnet_threshold)
        digitalWrite(step_pul[num1], motor_hl);
    }
    delayMicroseconds(max_time - slope * accel + accel * (i + 1));
  }
}

void move_arm(int arm, int arg) {
  if (arm == 0) servo0.write(deg[arm][arg]);
  else servo1.write(deg[arm][arg]);
}

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  for (int i = 0; i < 2; i++) {
    pinMode(step_dir[i], OUTPUT);
    pinMode(step_pul[i], OUTPUT);
    pinMode(sensor[i], INPUT);
  }
  servo0.attach(7);
  servo1.attach(8);
  servo0.write(deg[0][3]);
  servo1.write(deg[1][3]);
  //delay(70);
  digitalWrite(13, HIGH);
}

void loop() {
  //Serial.println(analogRead(sensor[0]));
  if (Serial.available()) {
    buf[idx] = Serial.read();
    if (buf[idx] == '\n') {
      buf[idx] = '\0';
      data[0] = atoi(strtok(buf, " "));
      data[1] = atoi(strtok(NULL, " "));
      data[2] = atoi(strtok(NULL, " "));
      if (data[1] >= 1000) move_arm(data[0], data[1] / 1000 - 1);
      else move_motor(data[0], data[1], data[2]);
      idx = 0;
    }
    else {
      idx++;
    }
  }
}
