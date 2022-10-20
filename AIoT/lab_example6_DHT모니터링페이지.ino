#include <DHT.h>
#include <Vegemite.h>

DHT dht(A1, DHT22);
Vegemite v;

uint32_t StartTime;
uint32_t DataCaptureDelay;

uint32_t getStartTime() {
  return millis() + DataCaptureDelay; //2초 간격으로 데이터 측정
}

void setup() {
  Serial.begin(250000); //vegemite를 사용할 때는 BR 250k가 필수임

  dht.begin();

  DataCaptureDelay=2000;
  StartTime=getStartTime();
}

void loop() {
  if(millis() > StartTime) { //2초 간격으로 온/습도 정보 받아옴
    float humidity=dht.readHumidity();
    float temperature=dht.readTemperature();

    if(!isnan(humidity) && !isnan(temperature)) { //vegemite를 통해 temperature, humidity 정보 전송
      v.send("temperature", temperature);
      v.send("humidity", humidity);
    }

    StartTime=getStartTime(); //실행 시간 초기화
  }
}
