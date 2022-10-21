#define LAMP 17

uint32_t TimeCompare;
uint32_t StartTime = 0;

int Hour=0;
int Minute=1;
int Second=0;

uint32_t TimeSum=(uint32_t) ((Hour*60+Minute)*60 +Second)*1000;

void setup() {
  // put your setup code here, to run once:
  pinMode(LAMP, OUTPUT);
  StartTime=millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  TimeCompare=(millis()-StartTime)/TimeSum;
  if(TimeCompare % 2==0) {
    digitalWrite(LAMP, HIGH) ;
  } else{
    digitalWrite(LAMP, LOW);
  }
}