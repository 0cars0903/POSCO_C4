import React from 'react';
import PageWrapper from 'components/internal/PageWrapper';
import NumberDisplay from 'components/NumberDisplay';

const Page: React.FC = function () {
  return (
    <PageWrapper title="DHT Status">
      <NumberDisplay label="Temperature" dataID="temperature" unit="C" />
      <NumberDisplay label="Humidity" dataID="hunidity" unit="%" />
    </PageWrapper>
  );
};

export default Page;
