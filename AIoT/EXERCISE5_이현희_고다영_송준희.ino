#include <DHT.h>
#include <AsyncTimer.h>
#include <Vegemite.h>
#include <SoftPWM.h>

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
  v.requestSubscription("config-auto");

//1번 코드
//1초 간격으로 온/습도, 토양습도 정보를 받아옴
  t.setInterval([]() { //온/습도 정보를 받아와서 vegemite로 전달
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    if (!isnan(humidity) && !isnan(temperature)) {
      v.send("temperature", temperature);
      v.send("humidity", humidity);
    }
  
    int soilMoist=map(analogRead(SOILMOIST_PIN), 0, 1023, 100, 0); //토양습도 정보를 받아와서 vegemite로 전달
    v.send("soilmoist", soilMoist);
  }, 1000);


  //2번 코드
  //vegemite에서 마지막으로 받아온 pump-water, config-light, config-fan에 대한 정보를 변수에 저장
  t.setInterval([]() {
    int autoConf = int(v.recv("config-auto"));
    int pumpWater = int(v.recv("pump-water")); 
    int lightConf = int(v.recv("config-light")); 
    int fanSpeed = int(v.recv("config-fan"));

   
    if (pumpWater == 1 && !currentPumpWorking) { // 화면에서 PUMP를 작동 
      currentPumpWorking = true;
      v.send("pump-water", 0);
      digitalWrite(PUMP_PIN, HIGH);

      t.setTimeout([]() { //5s 이후에 PUMP OFF
        digitalWrite(PUMP_PIN, LOW);
        currentPumpWorking = false;
      }, 5000);
    }

    digitalWrite(LAMP_PIN, lightConf==1 ? HIGH : LOW); // 화면에서 LED ON, OFF

    if (fanSpeed==0) {
      SoftPWM.set(0);
    }
    else if (fanSpeed==1) {
      SoftPWM.set(70);
    }
    else {
      SoftPWM.set(100);
    }
  }, 500);
}

void loop() {
  v.subscribe();
  t.handle();
}
