import React, { useEffect, useRef } from "react";
import MiniTypeWriter from "./MiniTypeWriter";
import { useSelector } from "react-redux";
import { RootState } from "@/store/store";
import mermaid from "mermaid";

interface Type12MiniProps {
  title: string;
  description: string;
  mermaidCode: string;
  slideIndex: number;
  isFullSizeGraph: boolean;
}
const Type12Mini = ({
  title,
  description,
  mermaidCode,
  slideIndex,
  isFullSizeGraph,
}: Type12MiniProps) => {
  const { currentColors, currentTheme } = useSelector(
    (state: RootState) => state.theme
  );
  const mermaidRef = useRef<HTMLDivElement>(null);
  const hasInitialized = useRef<boolean>(false);

  // Initialize Mermaid once
  useEffect(() => {
    if (!hasInitialized.current) {
      mermaid.initialize({
        startOnLoad: false,
        theme: "base",
        themeVariables: {
          primaryColor: currentColors.slideBox,
          primaryTextColor: currentColors.slideTitle,
          primaryBorderColor: currentColors.slideBox,
          lineColor: currentColors.chartColors[0],
          secondaryColor: currentColors.slideHeading,
          fontFamily: currentColors.fontFamily || "Inter",
          background: currentColors.background || "#ffffff",
        },
      });
      hasInitialized.current = true;
    }
  }, [currentColors]);

  // Render the diagram on code/theme change
  useEffect(() => {
    if (typeof window !== "undefined" && mermaidCode && mermaidRef.current) {
      const uniqueId = `mermaid-${slideIndex}-mini`;
      mermaid
        .render(uniqueId, mermaidCode)
        .then(({ svg }) => {
          if (mermaidRef.current) {
            mermaidRef.current.innerHTML = svg;

            // Optional: apply inline styling after render
            const svgEl = mermaidRef.current.querySelector("svg");
            if (svgEl) {
              svgEl.style.width = "90px";
              svgEl.style.maxWidth = "100%";
              svgEl.style.background = currentColors.background || "#ffffff";
              svgEl.style.color = currentColors.slideTitle || "#000000";
              svgEl.style.fontFamily = currentColors.fontFamily || "Inter";
            }
          }
        })
        .catch((err) => {
          console.error("Mermaid render error:", err);
        });
    }
  }, [mermaidCode, slideIndex, currentColors]);
  return (
    <div className="slide-container w-full aspect-video bg-white p-2 flex flex-col  justify-center rounded-lg text-[6px] border shadow-xl">
      <div className="text-center mb-2">
        <div className="font-semibold text-[10px] text-center slide-title truncate">
          <MiniTypeWriter text={title} />
        </div>
      </div>
      <div
        className={`flex  gap-2  w-full items-center  ${
          isFullSizeGraph ? " flex-col " : ""
        } `}
      >
        <div className={` w-[80%]`} ref={mermaidRef}>
          {/* <MiniCharts chartData={chartData} /> */}
        </div>
        {/* <div className="w-full h-full">

                </div> */}
        <div className="w-full text-gray-600 text-[8px] line-clamp-6 slide-description">
          <MiniTypeWriter text={description} />
        </div>
      </div>
      {/* <div className="grid grid-cols-2 gap-2">
             
                

                <div className="text-gray-600 text-[8px] line-clamp-6 slide-description">{description}</div>
            </div> */}
    </div>
  );
};

export default Type12Mini;
