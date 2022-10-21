import { FetchComponentWrapper } from "components/internal/FetchComponentWrapper";

retrun(
  // JSX 블럭
  <FetchComponentWrapper
    className={$.container}
    label={label}
    action={action}
    dataID={dataID}
    dataFetchCount={1}
  >
    <Stack direction="row" spacing={3} alignItems="center" className={$.box}>
      <Typography variant="h6">{`${min}${unit}`}</Typography>
      <Box width={360}>
        <Slider
          step={step}
          onChange={onChange}
          onChangeCommitted={onChangeCommitted}
          disabled={disabled}
          valueLabelDisplay="on"
          min={min}
          max={max}
          value={value}
        />
      </Box>
      <Typography variant="h6">{`${max}${unit}`}</Typography>
    </Stack>
    <span className={$.description}>{description}</span>
  </FetchComponentWrapper>
);
