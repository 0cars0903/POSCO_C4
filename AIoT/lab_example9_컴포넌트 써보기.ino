#include <DHT.h>
#include <AsyncTimer.h>
#include <Vegemite.h>

auto SOILMOIST_PIN = A6;
auto DHT22_PIN = A1;
auto PUMP_PIN = 16;
auto LAMP_PIN = 17;

DHT dht(DHT22_PIN, DHT22);
AsyncTimer t;
Vegemite v;

bool currentPumpWorking = false;


void setup() {
  Serial.begin(250000);
  dht.begin();

  pinMode(SOILMOIST_PIN, INPUT);
  pinMode(PUMP_PIN, OUTPUT);
  pinMode(LAMP_PIN, OUTPUT);

  v.requestSubscription("config-light"); //주기적으로 config-light 정보를 받아와라. 받아오는 주기는 vegemite가 알아서
  v.requestSubscription("pump-water");

  t.setInterval([]() {
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    if (!isnan(humidity) && !isnan(temperature)) {
      v.send("temperature", temperature);
      v.send("humidity", humidity);
    }

    int soilMoist=map(analogRead(SOILMOIST_PIN), 0, 1023, 100, 0);
    v.send("soilmoist", soilMoist);
  }, 1000);

  //2번
  t.setInterval([]() {
    int pumpWater = int(v.recv("pump-water")); // v.receive
    int lightConf = int(v.recv("config-light")); //최근에 가장 마지막에 받아온 config-light 값을 저장

    if (pumpWater == 1 && !currentPumpWorking) {
      currentPumpWorking = true;
      v.send("pump-water", 0);
      digitalWrite(PUMP_PIN, HIGH);
      t.setTimeout([]() { //5000ms 이후에 PUMP를 끈다
        digitalWrite(PUMP_PIN, LOW);
        currentPumpWorking = false;
      }, 5000);
    }

    digitalWrite(LAMP_PIN, lightConf==1 ? HIGH : LOW);
  }, 500);
}

void loop() {
  v.subscribe();
  t.handle();
}
