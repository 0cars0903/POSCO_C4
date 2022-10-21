import React from 'react';
import PageWrapper from 'components/internal/PageWrapper';
import NumberDisplay from 'components/NumberDisplay';
import ConditionLight from 'components/ConditionLight';
import PushButton from 'components/PushButton';
import ToggleSwitch from 'components/ToggleSwitch';
import ControlGroup from 'components/ControlGroup';

const Page: React.FC = function () {
  return (
    <PageWrapper title="IoT Web Component Example">
      <ControlGroup label="DHT Sensor">
        <NumberDisplay label="Temperature" dataID="temperature" unit="C" />
        <NumberDisplay label="Humidity" dataID="humidity" unit="%" />
        <ConditionLight
          label="Air Humidity Condition"
          dataID="humidity"
          coloringRule={(humidity: number) => (humidity < 85 ? '#00FF00' : '#FF0000')}
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
        <ToggleSwitch label="LED" dataID="config-light" />
      </ControlGroup>
    </PageWrapper>
  );
};

export default Page;
