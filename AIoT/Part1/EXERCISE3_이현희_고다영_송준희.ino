#include <U8g2lib.h> //U8g2 라이브러리 호출
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);
#define PUMP 16 //전처리문
#define SOILHUMI A6 //전처리문

uint32_t DataCaptureDelay=3000; //3초마다 데이터 측정을 위해 지연시간 설정
uint32_t DataCapture_ST=0; 

int Soilhumi=0;

//setup function
void setup() {
  u8g2.begin();
  Serial.begin(9600);
  pinMode(SOILHUMI, INPUT); //토양습도를 input으로 설정
  DataCapture_ST=millis(); //타이머 사용을 위한 시간 함수
  pinMode(PUMP, OUTPUT); //DC PUMP를 output으로 설정
}

void loop() {
  if((millis()-DataCapture_ST) > DataCaptureDelay) { //3초마다 온/습도 및 토양 습도 측정 
      Soilhumi=map(analogRead(SOILHUMI), 0, 1023, 100, 0); //0~1023까지의 analog data를 0~100까지 mapping해서 퍼센트로 표시

  if(isnan(Soilhumi)){ //오류가 발생했을 때 아래 구문 출력
    Serial.println(F("Failed to read from sensor!"));
    return;
  }

  if(Soilhumi<=30){ //토양 습도가 30 이하일 때 DC PUMP 동작
    digitalWrite(PUMP,HIGH);
    delay(2000);
  }
  else if (Soilhumi>=60){ //토양 습도가 60 이상일 때 DC PUMP OFF
    digitalWrite(PUMP, LOW);
    delay(2000);
    }
  OLEDdraw(); //토양 습도 표시
  DataCapture_ST=millis(); //실행 시간 초기화
  }
}

//OLEDdraw 함수
void OLEDdraw(){
  u8g2.clearBuffer(); //버퍼 비우기

  u8g2.setFont(u8g2_font_ncenB08_te); //폰트 설정
  u8g2.drawStr(1, 15, " AIBD AIOT"); 

  u8g2.drawStr(15, 36, "Soilhumi");
  u8g2.setCursor(85, 36); u8g2.print(Soilhumi);
  u8g2.drawStr(116, 36, "%");
 
  u8g2.sendBuffer();
}

