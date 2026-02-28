import React, { useState } from "react";
import { useSelector } from "react-redux";
import { RootState } from "@/store/store";
import { IconMapper } from "../../utils/IconList";

type Chart = {
  chart_type: string;
  icon?: string;
  value: {
    number_type: string;
    numerator?: number;
    denominator?: number;
    percentage?: number;
    numerical?: number;
    suffix?: string;
  };
};

const colors = [
  "#6453ff",
  "#22c1dd",
  "#ff6453",
  "#ffc122",
  "#22ddc1",
  "#c122ff",
  "#dd22ff",
  "#ff22c1",
  "#c1ff22",
  "#22ffc1",
];

const MiniInfoGraphics = ({
  slideIndex,
  itemIndex,
  chart,
}: {
  slideIndex: number;
  itemIndex: number;
  chart: Chart;
}) => {
  const { currentColors } = useSelector((state: RootState) => state.theme);

  const percentage =
    chart.value.number_type === "fraction" &&
    chart.value.numerator &&
    chart.value.denominator
      ? (chart.value.numerator / chart.value.denominator) * 100
      : chart.value.percentage || 0;

  return (
    <div>
      {chart.chart_type === "progress-dial" && (
        <MiniProgressDial
          color={currentColors.chartColors[0]}
          percentage={percentage}
        />
      )}
      {chart.chart_type === "radial-progress" && (
        <MiniRadialProgress
          color={currentColors.chartColors[0]}
          percentage={percentage}
          numerator={chart.value.numerator}
          denominator={chart.value.denominator}
          numberType={chart.value.number_type}
        />
      )}
      {chart.chart_type === "progress-ring" && (
        <MiniProgressRing
          color={currentColors.chartColors[0]}
          percentage={percentage}
          numerator={chart.value.numerator}
          denominator={chart.value.denominator}
          numberType={chart.value.number_type}
        />
      )}
      {chart.chart_type === "progress-bar" && (
        <MiniProgressBar
          color={currentColors.chartColors[0]}
          percentage={percentage}
        />
      )}
      {chart.chart_type === "icon-infographic" && (
        <MiniIconGraphics
          color={currentColors.chartColors[0]}
          icon={chart.icon || "star"}
          percentage={percentage}
        />
      )}
      {chart.chart_type === "text" && (
        <MiniTextInfographic
          iconBg={currentColors.iconBg}
          numerical={chart.value.numerical || 0}
        />
      )}
    </div>
  );
};

export default MiniInfoGraphics;

function MiniIconGraphics({
  color,
  icon,
  percentage,
}: {
  color: string;
  icon: string;
  percentage: number;
}) {
  const percentageValue = percentage > 100 ? 100 : percentage;
  const radius = 20;
  const circumference = 2 * Math.PI * radius;
  const gap = percentageValue === 100 ? 0 : 2;
  const adjustedCircumference = circumference - gap;

  return (
    <div className="relative w-12 h-12 mx-auto">
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 60 60">
        <circle
          className="text-gray-200"
          strokeWidth="6"
          stroke={color}
          opacity={0.3}
          fill="transparent"
          r={radius}
          cx="30"
          cy="30"
        />
        {percentageValue !== 0 && (
          <circle
            style={{ stroke: color }}
            strokeWidth="6"
            strokeLinecap={percentageValue === 100 ? "butt" : "round"}
            stroke="currentColor"
            fill="transparent"
            r={radius}
            cx="30"
            cy="30"
            strokeDasharray={`${adjustedCircumference}`}
            strokeDashoffset={
              ((100 - percentage) / 100) * adjustedCircumference + gap
            }
          />
        )}
      </svg>
      <div
        style={{ color: color }}
        className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-sm"
      >
        {IconMapper(true, icon)}
      </div>
    </div>
  );
}

function MiniProgressDial({
  color,
  percentage,
}: {
  color: string;
  percentage: number;
}) {
  const percentageValue = percentage > 100 ? 100 : percentage;
  const needleRotation = Math.round((percentageValue / 100) * 180 - 90);

  return (
    <div className="relative w-12 h-8 mx-auto">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80">
        <path
          d="M10,60 A 50,50 0 0,1 110,60"
          stroke={color}
          strokeWidth="12"
          fill="none"
        />
        <path
          d="M52,60 C52,57 68,57 68,60 L60,15 Z"
          fill={color}
          transform={`rotate(${needleRotation}, 60, 60)`}
        />
        <circle
          cx="60"
          cy="60"
          r="4"
          fill="white"
          stroke={color}
          strokeWidth="1.5"
        />
      </svg>
    </div>
  );
}

function MiniRadialProgress({
  color,
  percentage,
  numerator,
  denominator,
  numberType,
}: {
  color: string;
  percentage: number;
  numerator?: number;
  denominator?: number;
  numberType: string;
}) {
  const percentageValue = percentage > 100 ? 100 : percentage;
  const radius = 20;
  const arcLength = Math.PI * radius;
  const offset =
    percentageValue === 100 ? 0 : arcLength * (1 - percentageValue / 100);

  return (
    <div className="relative w-12 h-8 mx-auto">
      <svg className="w-full h-full" viewBox="0 0 60 30">
        <path
          className="text-gray-200"
          d="M6,30 A 24,24 0 0,1 54,30"
          strokeWidth="6"
          stroke={color}
          opacity={0.3}
          fill="none"
          strokeLinecap="round"
        />
        <path
          style={{ stroke: color }}
          strokeWidth="6"
          strokeLinecap="round"
          stroke="currentColor"
          fill="none"
          d="M6,30 A 24,24 0 0,1 54,30"
          strokeDasharray={`${arcLength}, ${arcLength}`}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 text-[10px] font-bold">
        <p style={{ color: color }}>
          {numberType === "fraction" && numerator && denominator
            ? `${numerator}/${denominator}`
            : `${percentage}%`}
        </p>
      </div>
    </div>
  );
}

function MiniProgressRing({
  color,
  percentage,
  numerator,
  denominator,
  numberType,
}: {
  color: string;
  percentage: number;
  numerator?: number;
  denominator?: number;
  numberType: string;
}) {
  const percentageValue = percentage > 100 ? 100 : percentage;
  const radius = 20;
  const circumference = 2 * Math.PI * radius;
  const gap = percentageValue === 100 ? 0 : 2;
  const adjustedCircumference = circumference - gap;

  return (
    <div className="relative w-12 h-12 mx-auto">
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 60 60">
        <circle
          className="text-gray-200"
          strokeWidth="6"
          stroke={color}
          opacity={0.3}
          fill="transparent"
          r={radius}
          cx="30"
          cy="30"
        />
        {percentageValue !== 0 && (
          <circle
            style={{ stroke: color }}
            strokeWidth="6"
            strokeLinecap={percentageValue === 100 ? "butt" : "round"}
            stroke="currentColor"
            fill="transparent"
            r={radius}
            cx="30"
            cy="30"
            strokeDasharray={`${adjustedCircumference}`}
            strokeDashoffset={
              ((100 - percentageValue) / 100) * adjustedCircumference + gap
            }
          />
        )}
      </svg>
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-[8px] font-bold">
        <p style={{ color: color }}>
          {numberType === "fraction" && numerator && denominator
            ? `${numerator}/${denominator}`
            : `${percentage}%`}
        </p>
      </div>
    </div>
  );
}

function MiniProgressBar({
  color,
  percentage,
}: {
  color: string;
  percentage: number;
}) {
  const percentageValue = percentage > 100 ? 100 : percentage;
  return (
    <div
      className="relative w-12 rounded-full mx-auto"
      style={{
        backgroundColor: "rgb(229 231 235)",
        height: "4px",
      }}
    >
      <div
        style={{ backgroundColor: color, width: `${percentageValue}%` }}
        className="absolute rounded-full inset-0"
      />
    </div>
  );
}

function MiniTextInfographic({
  iconBg,
  numerical,
}: {
  iconBg: string;
  numerical: number;
}) {
  const formatNumber = (value: number) => {
    if (isNaN(value)) {
      return value;
    }
    const absValue = Math.abs(value);
    if (absValue >= 1000000000) {
      return `${(absValue / 1000000000).toFixed(0)}B`;
    } else if (absValue >= 1000000) {
      return `${(absValue / 1000000).toFixed(0)}M`;
    } else if (absValue >= 1000) {
      return `${(absValue / 1000).toFixed(0)}k`;
    }
    return absValue.toString();
  };
  return (
    <div
      className="w-8 h-8  rounded-full  flex-col mx-auto mb-1 flex items-center justify-center"
      style={{ backgroundColor: iconBg }}
    >
      <p className="text-[10px] text-white">{formatNumber(numerical)}</p>
    </div>
  );
}
