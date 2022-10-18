#include <U8g2lib.h> //U8g2 라이브러리 호출
#include "DHT.h"  // DHT 라이브러리 호출
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);
#include <SoftPWM.h> //SoftPWM 라이브러리 호출

SOFTPWM_DEFINE_CHANNEL(A3);

#define DHTPIN A1 //전처리문
#define DHTTYPE DHT22 //전처리문


DHT dht(DHTPIN, DHTTYPE); //온도습도측정을 위한 라이브러리 함수 사용

uint32_t DataCaptureDelay=3000; //3초마다 데이터 측정을 위해 지연시간 설정
uint32_t DataCapture_ST=0; 

float Temp;
float Humi;
int PWM = 0; //DC FAN 제어 상태를 표시하기 위해 PWM 변수 선언

//setup function
void setup() {
  dht.begin();
  u8g2.begin();
  SoftPWM.begin(490);
  DataCapture_ST=millis(); //타이머 사용을 위한 시간 함수
}

void loop() {
  if((millis()-DataCapture_ST) > DataCaptureDelay) { //3초마다 온/습도 및 토양 습도 측정 
    Humi=dht.readHumidity(); //데이터 받아옴
    Temp=dht.readTemperature(); //데이터 받아옴
   
  if(isnan(Humi) ||isnan(Temp)){ //오류가 발생했을 때 아래 구문 출력
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  if(Temp>=30){ //30도 이상 측정 시, DC FAN ON(PWM:100)
    SoftPWM.set(100);
    delay(2000);
    PWM=100; 
  }    
  else if (Temp<=25){ //25도 이하 측정 시, DC FAN OFF(PWM:0)
    SoftPWM.set(0);
    delay(2000);
  }
  else{ //그 외, 25도부터 30도 사이에서는 DC FAN ON(PWM:65)
    SoftPWM.set(65);
    delay(2000);
    PWM=65;
  }

  OLEDdraw(); //OLED 화면 출력함수 호출
  DataCapture_ST=millis(); //실행 시간 초기화
  }
}

//OLEDdraw 함수
void OLEDdraw(){
  u8g2.clearBuffer(); //버퍼 비우기

  u8g2.setFont(u8g2_font_ncenB08_te); //폰트 설정
  u8g2.drawStr(1, 15, " AIBD AIOT"); 

  u8g2.drawStr(15, 36, "Temp.");
  u8g2.setCursor(85, 36);
  u8g2.print(Temp);
  u8g2.drawStr(114, 36, "\xb0");
  u8g2.drawStr(119, 36, "C");

  u8g2.drawStr(15, 47, "Humidity");
  u8g2.setCursor(85, 47); u8g2.print(Humi);
  u8g2.drawStr(116, 47, "%");
  

  u8g2.drawStr(15, 58, "DC FAN"); //DC FAN 제어상태를 OLED에 표시
  u8g2.setCursor(85, 58); 
  u8g2.print(PWM); //상태 표시

  u8g2.sendBuffer();
}

