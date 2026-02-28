import React, { useEffect, useRef } from "react";
import EditableText from "../EditableText";
import { useSelector } from "react-redux";
import SlideFooter from "./SlideFooter";
import { RootState } from "@/store/store";
import mermaid from "mermaid";

const Type12Layout = ({
  title,
  description,
  slideId,
  mermaidCode,
  slideIndex,
  isFullSizeGraph,
}: {
  title: string;
  description?: string;
  slideId: string | null;
  mermaidCode: string;
  slideIndex: number;
  isFullSizeGraph: boolean;
}) => {
  const { currentColors, currentTheme } = useSelector(
    (state: RootState) => state.theme
  );

  const mermaidRef = useRef<HTMLDivElement>(null);
  const hasInitialized = useRef<boolean>(false);

  // Initialize Mermaid once
  useEffect(() => {
    // if (!hasInitialized.current) {

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
        background: currentColors.slideBg || "#ffffff",
      },
    });
    hasInitialized.current = true;
    // }
  }, [currentColors]);

  // Render the diagram on code/theme change
  useEffect(() => {
    if (typeof window !== "undefined" && mermaidCode && mermaidRef.current) {
      const uniqueId = `mermaid-${slideIndex}`;
      mermaid
        .render(uniqueId, mermaidCode)
        .then(({ svg }) => {
          if (mermaidRef.current) {
            mermaidRef.current.innerHTML = svg;

            // Optional: apply inline styling after render
            const svgEl = mermaidRef.current.querySelector("svg");
            if (svgEl) {
              svgEl.style.width = "600px";
              svgEl.style.maxWidth = "100%";
              svgEl.style.background = currentColors.slideBox || "#ffffff";
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
    <div
      className="slide-container px-20 font-inter rounded-sm w-full max-w-[1280px] shadow-lg py-[86px] max-h-[720px] flex flex-col items-center justify-center aspect-video bg-white relative"
      data-slide-element
      data-slide-index={slideIndex}
      data-slide-id={slideId}
      data-slide-type="5"
      data-element-type="slide-container"
      data-element-id={`slide-${slideIndex}-container`}
      style={{
        fontFamily: currentColors.fontFamily || "Inter, sans-serif",
      }}
    >
      <EditableText
        slideIndex={slideIndex}
        elementId={`slide-${slideIndex}-title`}
        type="title"
        content={title}
        isAlingCenter={false}
      />
      <div
        className={`flex w-full items-center  mt-6 ${
          isFullSizeGraph ? "flex-col gap-10" : " gap-16"
        }`}
      >
        <div
          data-slide-element
          data-element-type="graph"
          data-graph-type="graph"
          data-element-id={`slide-group-${slideIndex}-graph`}
          className=" w-[80%] "
          ref={mermaidRef}
        />
        <div className="w-full text-center">
          <EditableText
            slideIndex={slideIndex}
            elementId={`slide-${slideIndex}-description-body`}
            type="description-body"
            isAlingCenter={isFullSizeGraph}
            content={description || ""}
          />
        </div>
      </div>
      <SlideFooter />
    </div>
  );
};

export default Type12Layout;
