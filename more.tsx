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
    <PageWrapper title="IoT Web Component Exercise 5">
      <ControlGroup label="Auto Mode">
        <ToggleSwitch label="Auto Mode" dataID="config-auto" />
      </ControlGroup>
      <ControlGroup label="Sensor">
        <NumberDisplay label="Temperature" dataID="temperature" unit="ºC" />
        <NumberDisplay label="Humidity" dataID="humidity" unit="%" />
        <NumberDisplay label="Soil Moisture" dataID="soilmoist" unit="%" />
      </ControlGroup>
      <ControlGroup label="Control">
        <ConditionLight
          label="Air Humidity Condition"
          dataID="humidity"
          coloringRule={(humidity: number) => (humidity < 85 ? '#00FF00' : '#FF0000')}
        />
        <PushButton
          label="Pump"
          dataID="pump-water"
          buttonText="Pump up"
          description="Push this button to pump water for 5 seconds"
        />
        <ConditionLight
          label="PUMP Condition"
          dataID="pump-water"
          coloringRule={(pumpwater: number) => (pumpwater === 0 ? '#df143c' : '#0080ff')} /// 조건문 true ? false :
        />
        <ToggleSwitch label="LED" dataID="config-light" />
        <SliderControl
          label="Fan Speed"
          dataID="config-fan"
          min={0}
          max={2}
          description="It takes few seconds to be applied."
        />
      </ControlGroup>

    </PageWrapper>
  );
};

export default Page;
