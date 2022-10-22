#include <U8g2lib.h>
#include <DHT.h>
#include <AsyncTimer.h>
#include <Vegemite.h>
#include <SoftPWM.h>
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

auto SOILMOIST_PIN = A6;
auto DHT22_PIN = A1;
auto FAN_PIN = A3;
auto PUMP_PIN = 16;
auto LAMP_PIN = 17;

SOFTPWM_DEFINE_CHANNEL(FAN_PIN);
DHT dht(DHT22_PIN, DHT22);
AsyncTimer t;
Vegemite v;

bool currentPumpWorking = false;

char*auto_mode = 'OFF';

void setup() {
  Serial.begin(250000);
  SoftPWM.begin(490);
  dht.begin();

  pinMode(SOILMOIST_PIN, INPUT);
  pinMode(PUMP_PIN, OUTPUT);
  pinMode(LAMP_PIN, OUTPUT);

//주기적으로 vegemite를 통해 config-light, config-fan, pump-water에 대한 정보를 받아옴. 
  v.requestSubscription("config-auto");
  v.requestSubscription("config-light"); 
  v.requestSubscription("config-fan");
  v.requestSubscription("pump-water");

//1번 코드
//1초 간격으로 온/습도, 토양습도 정보를 받아옴
  t.setInterval([]() { //온/습도 정보를 받아와서 vegemite로 전달
    int autoConf = int(v.recv("config-auto"));
    
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    if (!isnan(humidity) && !isnan(temperature)) {
      v.send("temperature", temperature);
      v.send("humidity", humidity);
    }
  
    int soilMoist=map(analogRead(SOILMOIST_PIN), 0, 1023, 100, 0); //토양습도 정보를 받아와서 vegemite로 전달
    v.send("soilmoist", soilMoist);

    if (autoConf==1) {
      auto_mode = "ON";
      if(temperature > 25){
        digitalWrite(LAMP_PIN, HIGH);
      }
      else {
        digitalWrite(LAMP_PIN, LOW);
      }

      if (humidity > 30) {
        SoftPWM.set(100);
        delay(2000);
      }
      else {
        SoftPWM.set(0);
        delay(2000);
      }

      if (humidity < 60){
        digitalWrite(PUMP_PIN, HIGH);
      }
      else {
        digitalWrite(PUMP_PIN, LOW);
      }
    } 
    

    else if (autoConf == 0) {
      auto_mode = "OFF";
      t.setInterval([]() {
        int pumpWater = int(v.recv("pump-water"));
        int lightConf = int(v.recv("config-light"));
        int fanSpeed = int(v.recv("config-fan"));

        if (pumpWater == 1 && !currentPumpWorking) {
          currentPumpWorking = true;
          v.send("pump-water", 0);
          digitalWrite(PUMP_PIN, HIGH);
          t.setTimeout([]() {
            digitalWrite(PUMP_PIN, LOW);
            currentPumpWorking = false;
          }, 5000);
        }

        digitalWrite(LAMP_PIN, lightConf==1? HIGH : LOW);
        if (fanSpeed==0) {
          SoftPWM.set(0);}
        else if (fanSpeed==1) {
          SoftPWM.set(70);}
        else {
          SoftPWM.set(100);} 
      }, 500);
    }
    OLEDdraw();    
  }, 1000);
}

void loop() {
  int autoConf = int(v.recv("config-auto"));
  if (autoConf==1) {
    char*auto_mode = 'ON';
  
  if (autoConf==0) {
    char*auto_mode = 'OFF';
  }
  OLEDdraw();
  }
  v.subscribe();
  t.handle();
}

void OLEDdraw(){
  u8g2.clearBuffer(); //버퍼 비우기
  u8g2.setFont(u8g2_font_ncenB08_te); //폰트 설정

  u8g2.drawStr(1, 15, " AIBD AIOT");
  u8g2.drawStr(15, 36, "Automode"); //Automode를 OLED에 표시
  u8g2.setCursor(40, 36);
  u8g2.print(auto_mode);

  u8g2.sendBuffer();  
}