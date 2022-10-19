#include <U8g2lib.h> //U8g2 라이브러리 호출
#include "DHT.h"  // DHT 라이브러리 호출
#include <SoftPWM.h> //SoftPWM 라이브러리 호출
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

SOFTPWM_DEFINE_CHANNEL(A3);

//전처리문
#define DHTPIN A1 
#define DHTTYPE DHT22
#define SOILHUMI A6
#define LAMP 17
#define PUMP 16

DHT dht(DHTPIN, DHTTYPE); //온도습도측정을 위한 라이브러리 함수 사용

uint32_t DataCaptureDelay=2000; //2초
uint32_t DataCaptureDelay2=3000; //3초
uint32_t DataCapture_ST1=0; //2초마다 데이터 측정
uint32_t DataCapture_ST2=0; //3초마다 데이터 측정

uint32_t TimeCompare; 
uint32_t StartTime=0;

float Temp;
float Humi;
int Soilhumi=0;

int PWM = 0; //DC FAN 

int Hour=0;
int Minute=1;
int Second=0;

char* state="ON"; //DC PUMP 동작 상태

uint32_t TimeSum=(uint32_t) ((Hour*60 + Minute)*60+Second)*1000; //ms로 변환


//setup function
void setup() {
  dht.begin();
  u8g2.begin();
  SoftPWM.begin(490);
  pinMode(LAMP, OUTPUT);
  pinMode(PUMP, OUTPUT);
  pinMode(SOILHUMI, INPUT);
  StartTime=millis();
  DataCapture_ST1=millis(); 
  DataCapture_ST2=millis(); 
}

void loop() {
  TimeCompare=(millis()-StartTime)/TimeSum; //1분 간격을 0,1,2,3,, 순으로 mapping

//1분 간격으로 LED ON/OFF
  if(TimeCompare % 2==0) { //짝수의 경우 LED ON
    digitalWrite(LAMP, HIGH) ;
  } 
  else{ //홀수의 경우 LED OFF
    digitalWrite(LAMP, LOW);
  }

//2초마다 온/습도 측정
  if((millis()-DataCapture_ST1) > DataCaptureDelay) { 
    Humi=dht.readHumidity();
    Temp=dht.readTemperature(); 
    if(isnan(Humi)||isnan(Temp)){ 
      Serial.println(F("Failed to read from sensor!"));
      return;
    }
    DataCapture_ST1=millis(); 
    OLEDdraw(); 
  }

//3초마다 토양습도 측정
  if((millis()-DataCapture_ST2) > DataCaptureDelay2) {  
    Soilhumi=map(analogRead(SOILHUMI), 0, 1023, 100, 0);
    if (isnan(Soilhumi)){
      Serial.println(F("Failed to read from sensor!"));
      return;
    }
    DataCapture_ST2=millis(); 
    OLEDdraw();
    }
  
  if(Temp>=29){ //29도 이상일 때 DC FAN ON(PWM:100)
    SoftPWM.set(100);
    delay(2000);
    PWM=100; 
  }    
  else if (Temp<=20){ //20도 이하일 때, DC FAN OFF(PWM:0)
    SoftPWM.set(0);
    delay(2000);
  }
  else{ //그 사이에서는 DC FAN ON(PWM:65)
    SoftPWM.set(65);
    delay(2000);
    PWM=65;
  }

  if ((Soilhumi>=30) && (Soilhumi<=60)) { //토양 습도 30%~60% 일 때 DC PUMP ON
    digitalWrite(PUMP, HIGH);
    delay(2000);
  }
  else {
    digitalWrite(PUMP, LOW);
    delay(2000);
    state="OFF";
  }
}

//OLEDdraw 함수
void OLEDdraw(){
  u8g2.clearBuffer(); //버퍼 비우기

  u8g2.setFont(u8g2_font_ncenB08_te); //폰트 설정
  u8g2.drawStr(15, 10, "Temp."); //온도를 OLED에 표시
  u8g2.setCursor(85, 10);
  u8g2.print(Temp);
  u8g2.drawStr(114, 10, "\xb0");
  u8g2.drawStr(119, 10, "C");

  u8g2.drawStr(15, 21, "Humidity"); //습도를 OLED에 표시
  u8g2.setCursor(85, 21); u8g2.print(Humi);
  u8g2.drawStr(116, 21, "%");
  
  u8g2.drawStr(15, 32, "Soilhumi"); //토양 습도를 OLED에 표시
  u8g2.setCursor(85, 32); u8g2.print(Soilhumi);
  u8g2.drawStr(116, 32, "%");  

  u8g2.drawStr(15, 43, "DC FAN"); //DC FAN 제어상태를 OLED에 표시
  u8g2.setCursor(85, 43); 
  u8g2.print(PWM);

  u8g2.drawStr(15, 54, "LED"); //LED 작동 주기를 OLED에 표시
  u8g2.setCursor(80, 54); 
  u8g2.print(TimeSum); //상태 표시
  u8g2.println("ms");
    
  u8g2.drawStr(15, 63, "DC PUMP"); //DC PUMP 동작 상태를 OLED에 표시
  u8g2.setCursor(85, 63); 
  u8g2.println(state);
  
  u8g2.sendBuffer();
}
