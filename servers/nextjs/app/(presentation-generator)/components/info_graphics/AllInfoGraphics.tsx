import React, { useState } from "react";

import {
  Sheet,
  SheetContent,
  SheetFooter,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { useDispatch, useSelector } from "react-redux";
import { updateInfographicsChart } from "@/store/slices/presentationGeneration";
import { RootState } from "@/store/store";
import { getPercentage, ICON_LIST, IconMapper } from "../../utils/IconList";

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

const CHART_TYPES = [
  { value: "progress-dial", label: "Progress Dial" },
  { value: "radial-progress", label: "Radial Progress" },
  { value: "progress-ring", label: "Progress Ring" },
  { value: "progress-bar", label: "Progress Bar" },
  { value: "icon-infographic", label: "Icon Infographic" },
];

const AllInfoGraphics = ({
  slideIndex,
  itemIndex,
  chart,
}: {
  slideIndex: number;
  itemIndex: number;
  chart: Chart;
}) => {
  const dispatch = useDispatch();

  const [isEditingOpen, setIsEditingOpen] = useState(false);
  const [lineWeight, setLineWeight] = useState(20);
  const [selectedIcon, setSelectedIcon] = useState(chart.icon || "star");
  const [chartType, setChartType] = useState(chart.chart_type);

  // State for both percentage and fraction
  const [percentageValue, setPercentageValue] = useState(
    chart.value.number_type === "fraction"
      ? getPercentage(chart.value.numerator!, chart.value.denominator!)
      : chart.value.percentage || 0
  );
  const [numerator, setNumerator] = useState(chart.value.numerator || 0);
  const [denominator, setDenominator] = useState(
    chart.value.denominator || 100
  );
  const [numberType, setNumberType] = useState(chart.value.number_type);
  const { currentColors } = useSelector((state: RootState) => state.theme);

  const handlePercentageChange = (value: number) => {
    const newValue = Math.min(1000, Math.max(0, value));
    setPercentageValue(newValue);

    if (numberType === "fraction") {
      // Update numerator based on percentage while keeping denominator same
      const newNumerator = Math.round((newValue / 100) * denominator);
      setNumerator(newNumerator);
    }
  };

  const handleFractionChange = (num: number | null, den: number | null) => {
    // Ensure we have valid numbers
    const validNum = num !== null ? Math.max(0, num) : numerator;
    const validDen = den !== null ? Math.max(1, den) : denominator;

    setNumerator(validNum);
    setDenominator(validDen);

    // Calculate and update percentage
    const newPercentage = getPercentage(validNum, validDen);
    setPercentageValue(newPercentage);
  };

  const handlePercentageInputChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = e.target.value;
    if (value === "") {
      setPercentageValue(0); // Keep internal state at 0
      return;
    }
    handlePercentageChange(Number(value));
  };

  const handlePercentageBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    if (e.target.value === "") {
      handlePercentageChange(0);
    }
  };

  const handleNumeratorChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value === "") {
      setNumerator(0); // Keep internal state at 0
      return;
    }
    handleFractionChange(Number(value), null);
  };

  const handleNumeratorBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    if (e.target.value === "") {
      handleFractionChange(0, null);
    }
  };

  const handleDenominatorChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (value === "") {
      setDenominator(1); // Keep internal state at 1
      return;
    }
    handleFractionChange(null, Number(value));
  };

  const handleDenominatorBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    if (e.target.value === "") {
      handleFractionChange(null, 1);
    }
  };

  const handleContentEdit = (e: React.FormEvent<HTMLParagraphElement>) => {
    const content = e.currentTarget.textContent || "";

    // Check if content is in fraction format (e.g., "3/4")
    if (content.includes("/")) {
      const [num, den] = content.split("/").map((n) => parseInt(n));
      if (!isNaN(num) && !isNaN(den) && den !== 0) {
        setNumberType("fraction");
        handleFractionChange(num, den);
      }
    }
    // Check if content is in percentage format (e.g., "75%")
    else {
      const value = parseInt(content.replace("%", ""));
      if (!isNaN(value)) {
        setNumberType("percentage");
        handlePercentageChange(value);
      }
    }
  };

  const handleSave = () => {
    const chartData = {
      chart_type: chartType,
      value: {
        number_type: numberType,
      },
    } as Chart;

    // Add icon if it's an icon infographic
    if (chartType === "icon-infographic") {
      chartData.icon = selectedIcon;
    }

    // Add values based on number type
    if (numberType === "fraction") {
      chartData.value.numerator = numerator;
      chartData.value.denominator = denominator;
    } else if (numberType === "percentage") {
      chartData.value.percentage = percentageValue;
    }
    dispatch(
      updateInfographicsChart({
        slideIndex: slideIndex,
        itemIdx: itemIndex,
        chart: chartData,
      })
    );

    setIsEditingOpen(false);
  };
  const handleSheetClose = () => {
    handleSave();
    setIsEditingOpen(false);
  };

  const handleInfographicClick = (e: React.MouseEvent<HTMLDivElement>) => {
    e.stopPropagation();
    if (chartType !== "text") {
      setIsEditingOpen(true);
    }
  };

  return (
    <>
      <div
        onClick={handleInfographicClick}
        key={chart.chart_type}
        data-slide-element
        data-element-type="graph"
        data-graph-type="progress"
        data-element-id={`slide-group-${slideIndex}-item-${itemIndex}-graph`}
        className={` max-md:pointer-events-none ${
          chartType === "text" ? "cursor-default" : "cursor-pointer"
        }`}
      >
        {chartType === "progress-dial" && (
          <ProgressDial
            color={currentColors.chartColors[0]}
            percentage={percentageValue}
          />
        )}
        {chartType === "radial-progress" && (
          <RadialProgress
            strokeWidth={lineWeight}
            color={currentColors.chartColors[0]}
            percentage={percentageValue}
            numerator={numerator}
            denominator={denominator}
            onContentEdit={handleContentEdit}
            numberType={numberType}
          />
        )}
        {chartType === "progress-ring" && (
          <ProgressRing
            color={currentColors.chartColors[0]}
            percentage={percentageValue}
            numerator={numerator}
            denominator={denominator}
            lineWeight={lineWeight}
            onContentEdit={handleContentEdit}
            numberType={numberType}
          />
        )}
        {chartType === "progress-bar" && (
          <ProgressBar
            progressBg={currentColors.chartColors[2]}
            color={currentColors.chartColors[0]}
            percentage={percentageValue}
            lineWeight={lineWeight}
          />
        )}
        {chartType === "icon-infographic" && (
          <IconGraphics
            color={currentColors.chartColors[0]}
            icon={selectedIcon}
            percentage={percentageValue}
          />
        )}
        {chartType === "text" && (
          <TextInfographic
            dispatch={dispatch}
            slideIndex={slideIndex}
            itemIndex={itemIndex}
            item={chart}
            suffix={chart.value.suffix || ""}
            numerical={chart.value.numerical || 0}
            iconBg={currentColors.iconBg}
          />
        )}
      </div>

      <Sheet open={isEditingOpen} onOpenChange={handleSheetClose} modal={false}>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>Chart Settings</SheetTitle>
          </SheetHeader>

          <div className="grid gap-4 py-4">
            <div className="space-y-2">
              <Label>Chart Type</Label>
              <Select value={chartType} onValueChange={setChartType}>
                <SelectTrigger>
                  <SelectValue placeholder="Select chart type" />
                </SelectTrigger>
                <SelectContent>
                  {CHART_TYPES.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between mb-4">
                <Label>Display Format</Label>
                <Select value={numberType} onValueChange={setNumberType}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Select format" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="percentage">Percentage</SelectItem>
                    <SelectItem value="fraction">Fraction</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Percentage</Label>
                <div className="flex items-center space-x-4">
                  <div className="flex-1">
                    <Slider
                      value={[percentageValue]}
                      max={100}
                      step={1}
                      onValueChange={(value) => {
                        handlePercentageChange(value[0]);
                      }}
                    />
                  </div>
                  <div className="w-20">
                    <Input
                      type="number"
                      value={percentageValue || ""}
                      onChange={handlePercentageInputChange}
                      onBlur={handlePercentageBlur}
                      min={0}
                    />
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <Label>Fraction</Label>
                <div className="flex items-center space-x-2">
                  <Input
                    type="number"
                    value={numerator || ""}
                    onChange={handleNumeratorChange}
                    onBlur={handleNumeratorBlur}
                    min={0}
                    className="w-20"
                  />
                  <span className="text-lg">/</span>
                  <Input
                    type="number"
                    value={denominator || ""}
                    onChange={handleDenominatorChange}
                    onBlur={handleDenominatorBlur}
                    min={1}
                    className="w-20"
                  />
                  <div className="ml-2 text-sm text-muted-foreground">
                    = {percentageValue.toFixed(1)}%
                  </div>
                </div>
              </div>
            </div>

            {chartType === "icon-infographic" && (
              <div className="space-y-2">
                <Label>Icons</Label>
                <div className="grid grid-cols-6 gap-2 max-h-[200px] custom_scrollbar overflow-y-auto p-2 border rounded-md">
                  {Object.entries(ICON_LIST).map(([key, Icon]) => (
                    <button
                      key={key}
                      className={` rounded-lg border-2 hover:bg-slate-100 transition-colors ${
                        selectedIcon === key
                          ? "border-primary bg-slate-100"
                          : "border-transparent"
                      }`}
                      onClick={() => setSelectedIcon(key)}
                    >
                      {IconMapper(false, key)}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
          <SheetFooter>
            <Button
              className="w-full mt-8 bg-primary text-white"
              onClick={handleSave}
            >
              Save
            </Button>
          </SheetFooter>
        </SheetContent>
      </Sheet>
    </>
  );
};

export default AllInfoGraphics;

export function IconGraphics({
  color,
  icon,
  percentage,
}: {
  color: string;
  icon: string;
  percentage?: number;
}) {
  const percentageValue = percentage && percentage > 100 ? 100 : percentage;
  const radius = 110;
  const circumference = 2 * Math.PI * radius;
  const gap = percentageValue === 100 ? 0 : 10; // No gap at 100%
  const adjustedCircumference = circumference - gap;

  return (
    <div className="relative w-28 h-28 lg:w-44 lg:h-44  xl:w-48 xl:h-48 mx-auto md:mb-6">
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 240 240">
        <circle
          strokeWidth="20"
          stroke={color}
          opacity={0.3}
          fill="transparent"
          r={radius}
          cx="120"
          cy="120"
        />
        {percentageValue !== 0 && (
          <circle
            style={{ stroke: color }}
            strokeWidth="20"
            strokeLinecap={percentageValue! >= 100 ? "butt" : "round"}
            stroke="currentColor"
            fill="transparent"
            r={radius}
            cx="120"
            cy="120"
            strokeDasharray={`${adjustedCircumference}`}
            strokeDashoffset={
              ((100 - percentageValue!) / 100) * adjustedCircumference + gap
            }
          />
        )}
      </svg>
      <div
        style={{ color: color }}
        className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-4xl font-bold"
      >
        {IconMapper(false, icon)}
      </div>
    </div>
  );
}

export function ProgressDial({
  color,
  percentage,
}: {
  color: string;
  percentage?: number;
}) {
  // Calculate needle rotation based on percentage
  const needleRotation = Math.round((percentage! / 100) * 180 - 90);

  return (
    <div className="relative w-32 h-20 lg:w-56 lg:h-44 xl:w-64 xl:h-48 mx-auto md:mb-6 flex justify-center items-center">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 120">
        {/* Background arc */}
        <path
          d="M10,100 A 90,90 0 0,1 190,100"
          stroke={color}
          strokeWidth="20"
          fill="none"
        />

        {/* Needle */}
        <path
          id="needle"
          d="M92,100 C92,95 108,95 108,100 L100,20 Z"
          fill={color}
          transform={`rotate(${needleRotation}, 100, 100)`}
        />

        {/* Center circle */}
        <circle
          cx="100"
          cy="100"
          r="8"
          fill="white"
          stroke={color}
          strokeWidth="2"
        />
      </svg>
    </div>
  );
}

export function RadialProgress({
  strokeWidth,
  color,
  percentage,
  numerator,
  denominator,
  onContentEdit,
  numberType = "percentage",
}: {
  strokeWidth: number;
  color: string;
  percentage?: number;
  numerator?: number;
  denominator?: number;
  onContentEdit?: (e: React.FormEvent<HTMLParagraphElement>) => void;
  numberType?: string;
}) {
  const percentageValue =
    percentage && percentage > 100 ? 100 : percentage ?? 0;
  const radius = 90;
  const arcLength = Math.PI * radius;
  const strokeDasharray = arcLength;

  const correctionFactor = percentageValue === 100 ? 1 : 0.98;
  const strokeDashoffset =
    arcLength * (1 - (percentageValue / 100) * correctionFactor);

  return (
    <div className="relative w-32 h-20 lg:w-56 lg:h-44 xl:w-64 xl:h-48 mx-auto md:mb-6">
      <svg className="w-full h-full" viewBox="0 0 200 120">
        {/* Background half-circle */}
        <path
          strokeWidth="15"
          stroke={color}
          strokeLinecap="round"
          opacity={0.3}
          fill="transparent"
          d="M10,100 A 90,90 0 0,1 190,100"
        />

        {/* Foreground half-circle */}
        <path
          stroke={color}
          strokeWidth="15"
          strokeLinecap="round"
          fill="transparent"
          d="M10,100 A 90,90 0 0,1 190,100"
          strokeDasharray={strokeDasharray}
          strokeDashoffset={strokeDashoffset}
        />
      </svg>

      <div className="absolute top-[65%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-4xl font-bold">
        <p
          onClick={(e) => {
            const selection = window.getSelection();
            const range = document.createRange();
            range.selectNodeContents(e.currentTarget);
            selection?.removeAllRanges();
            selection?.addRange(range);
          }}
          onInput={onContentEdit}
          style={{ color }}
          className="text-[24px] focus-visible:outline-none leading-[32px] font-bold"
        >
          {numberType === "fraction" && numerator && denominator
            ? `${numerator}/${denominator}`
            : `${percentageValue}%`}
        </p>
      </div>
    </div>
  );
}

export function ProgressRing({
  color,
  percentage,
  numerator,
  denominator,
  lineWeight = 20,
  onContentEdit,
  numberType = "percentage",
}: {
  color: string;
  percentage?: number;
  numerator?: number;
  denominator?: number;
  lineWeight?: number;
  onContentEdit?: (e: React.FormEvent<HTMLParagraphElement>) => void;
  numberType?: string;
}) {
  const percentageValue = percentage && percentage > 100 ? 100 : percentage;
  const radius = 110;
  const circumference = 2 * Math.PI * radius;
  const gap = percentageValue === 100 ? 0 : 10; // No gap at 100%
  const adjustedCircumference = circumference - gap;

  return (
    <div className="relative w-28 h-28 lg:w-44 lg:h-44  xl:w-48 xl:h-48 mx-auto md:mb-6">
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 240 240">
        <circle
          strokeWidth="20"
          stroke={color}
          opacity={0.3}
          fill="transparent"
          r={radius}
          cx="120"
          cy="120"
        />
        {percentageValue !== 0 && (
          <circle
            style={{ stroke: color }}
            strokeWidth="20"
            strokeLinecap={percentageValue === 100 ? "butt" : "round"}
            stroke="currentColor"
            fill="transparent"
            r={radius}
            cx="120"
            cy="120"
            strokeDasharray={`${adjustedCircumference}`}
            strokeDashoffset={
              ((100 - percentageValue!) / 100) * adjustedCircumference + gap
            }
          />
        )}
      </svg>
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-4xl font-bold">
        <p
          onClick={(e) => {
            const selection = window.getSelection();
            const range = document.createRange();
            range.selectNodeContents(e.currentTarget);
            selection?.removeAllRanges();
            selection?.addRange(range);
          }}
          onInput={onContentEdit}
          contentEditable
          suppressContentEditableWarning
          style={{ color: color }}
          className="text-base md:text-[24px] focus-visible:outline-none leading-[32px] font-bold"
        >
          {numberType === "fraction" && numerator && denominator
            ? `${numerator}/${denominator}`
            : `${percentage}%`}
        </p>
      </div>
    </div>
  );
}

export function ProgressBar({
  progressBg,
  color,
  percentage,
  lineWeight = 20,
}: {
  progressBg: string;
  color: string;
  percentage?: number;
  lineWeight?: number;
}) {
  const percentageValue = percentage && percentage > 100 ? 100 : percentage;
  return (
    <div
      className={`relative w-full  rounded-full mx-auto  mb-6 `}
      style={{
        backgroundColor: progressBg,

        height: `${lineWeight}px`,
      }}
    >
      <div
        style={{ backgroundColor: color, width: `${percentageValue}%` }}
        className="absolute rounded-full inset-0 flex items-center justify-center"
      />
    </div>
  );
}
export function TextInfographic({
  dispatch,
  iconBg,
  slideIndex,
  itemIndex,
  item,
  suffix,
  numerical,
}: {
  dispatch: any;
  slideIndex: number;
  itemIndex: number;
  item: any;
  suffix: string;
  numerical: number;
  iconBg: string;
}) {
  const updateChart = ({
    slideIndex,
    itemIdx,
    chart,
  }: {
    slideIndex: number;
    itemIdx: number;
    chart: any;
  }) => {
    dispatch(updateInfographicsChart({ slideIndex, itemIdx, chart }));
  };
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
      style={{ backgroundColor: iconBg }}
      className="w-28 h-28 lg:w-44 lg:h-44  xl:w-48 xl:h-48 mx-auto rounded-full  flex items-center justify-center mb-6"
    >
      <div
        className={`text-center text-white cursor-text ${
          suffix.length === 1 ? "flex items-center gap-1" : ""
        }`}
      >
        <p
          onBlur={(e) => {
            updateChart({
              slideIndex,
              itemIdx: itemIndex,
              chart: {
                chart_type: item.chart_type,
                value: {
                  number_type: item.value.number_type,
                  numerical: e.currentTarget.innerText,
                  suffix: item.value.suffix,
                },
              },
            });
          }}
          contentEditable={true}
          suppressContentEditableWarning
          className="text-base md:text-[24px] focus-visible:outline-none leading-[40px] font-bold"
        >
          {formatNumber(numerical)}
        </p>
        <p
          onBlur={(e) => {
            updateChart({
              slideIndex,
              itemIdx: itemIndex,
              chart: {
                chart_type: item.chart_type,
                value: {
                  number_type: item.value.number_type,
                  numerical: item.value.numerical,
                  suffix: e.currentTarget.innerText,
                },
              },
            });
          }}
          contentEditable={true}
          suppressContentEditableWarning
          className="text-base  md:text-[20px] cursor-text focus-visible:outline-none leading-[24px] font-bold"
        >
          {suffix.toString().replace(/\*\*/g, "")}
        </p>
      </div>
    </div>
  );
}
