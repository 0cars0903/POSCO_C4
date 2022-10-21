import React from 'react';
import PageWrapper from 'components/internal/PageWrapper';
import NumberDisplay from 'components/NumberDisplay';
import ConditionLight from 'components/ConditionLight';
import PushButton from 'components/PushButton';
import ToggleSwitch from 'components/ToggleSwitch';
import SliderControl from 'components/SliderControl';
import ControlGroup from 'components/ControlGroup';

const Page: React.FC = function () {
  return (
    <PageWrapper title="IoT Web Component Example">
      <ControlGroup label="Auto mode">
        <ToggleSwitch label="Auto Mode" dataID="config-auto" />
      </ControlGroup>
      <ControlGroup label="DHT Sensor">
        <NumberDisplay label="Temperature" dataID="temperature" unit="C" />
        <ConditionLight
          label="Temperature Condition"
          dataID="temperature"
          coloringRule={(temperature: number) => (temperature < 25 ? '#00FF00' : '#FF0000')} /// 조건문 true ? false :
        />
        <NumberDisplay label="Humidity" dataID="humidity" unit="%" />
        <ConditionLight
          label="Air Humidity Condition"
          dataID="humidity"
          coloringRule={(humidity: number) => (humidity < 85 ? '#00FF00' : '#FF0000')} /// 조건문 true ? false :
        />
      </ControlGroup>
      <ControlGroup label="Soil Control">
        <NumberDisplay label="soil Moisture" dataID="soilmoist" unit="%" />
        <PushButton
          label="Pump"
          dataID="pump-water"
          buttonText="Pump up"
          description="Push this button to pump water for 5 seconds"
        />
        <ConditionLight
          label="PUMP Condition"
          dataID="pump-water"
          coloringRule={(pump-water: number) => (pump-water = 1 ? '#df143c' : '#0080ff')} /// 조건문 true ? false :
        />
        <ToggleSwitch label="LED" dataID="config-light" />
      </ControlGroup>
      <ControlGroup label="Fan Control">
        <SliderControl
          label="Fan Speed"
          dataID="confing-fan"
          min={0}
          max={100}
          description="It takes few seconds to be applied"
          unit="%"
        />
      </ControlGroup>
    </PageWrapper>
  );
};

export default Page;
