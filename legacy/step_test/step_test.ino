void setup() {
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
}

void loop() {
  //digitalWrite(9, HIGH);
  digitalWrite(11, HIGH);
  bool hl = true;
  while(1){
    hl = !hl;
    //digitalWrite(10, hl);
    digitalWrite(12, hl);
    delayMicroseconds(500);
  }

}
