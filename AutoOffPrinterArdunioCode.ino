int ledPin = 13;
char data;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    data = Serial.read();
    if (data == '1') {
      digitalWrite(ledPin, LOW);
    } else if (data == '0') {
      digitalWrite(ledPin, HIGH);
    }
  }
}
