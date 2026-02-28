import React from "react";
import EditableText from "../EditableText";
import ElementMenu from "../ElementMenu";
import { MoreVertical, Plus } from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import {
  addInfographics,
  deleteInfographics,
  updateSlideVariant,
} from "@/store/slices/presentationGeneration";
import AllInfoGraphics from "../info_graphics/AllInfoGraphics";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@radix-ui/react-popover";
import { RootState } from "@/store/store";
import SlideFooter from "./SlideFooter";

type Type10LayoutProps = {
  title: string;
  slideIndex: number;
  slideId: string | null;
  description: string;
  design_index: number;
  infographics: {
    title: string;
    description: string;
    chart: {
      chart_type: string;
      value: {
        number_type: string;
        numerical: number;
        suffix: string;
        numerator?: number;
        denominator?: number;
        percentage?: number;
      };
    };
  }[];
};

const Type10Layout = ({
  title,
  slideIndex,
  slideId,
  infographics,
  description,
  design_index,
}: Type10LayoutProps) => {
  const { currentColors } = useSelector((state: RootState) => state.theme);
  const dispatch = useDispatch();

  const handleDeleteItem = (index: number) => {
    dispatch(
      deleteInfographics({
        slideIndex: slideIndex,
        itemIdx: index,
      })
    );
  };
  const handleAddItem = () => {
    dispatch(
      addInfographics({
        slideIndex: slideIndex,
        item: {
          title: "Enter Title",
          description: "Enter Description",
          chart: {
            chart_type: infographics[0].chart.chart_type,
            value: {
              percentage: 80,
              number_type: "percentage",
            },
          },
        },
      })
    );
  };
  const handleVariantChange = (newVariant: number) => {
    dispatch(updateSlideVariant({ index: slideIndex, variant: newVariant }));
  };

  const VariantMenu = () => (
    <Popover>
      <PopoverTrigger asChild>
        <button className="absolute hidden lg:block  top-0 -left-7 p-1 rounded-md bg-white shadow-md opacity-0 group-hover:opacity-100 transition-opacity hover:bg-gray-50 z-50">
          <MoreVertical className="w-4 h-4 text-black" />
        </button>
      </PopoverTrigger>
      <PopoverContent align="start" className="w-[180px] z-50 p-2 bg-white">
        <button
          onClick={() => handleVariantChange(1)}
          className={`w-full text-base font-medium py-2 hover:bg-gray-200 transition-colors rounded-md  bg-transparent ${
            design_index === 1 ? "bg-gray-200" : ""
          }`}
        >
          With Background
        </button>
        <button
          onClick={() => handleVariantChange(2)}
          className="w-full text-base font-medium py-2 hover:bg-gray-200 transition-colors rounded-md  bg-transparent"
        >
          Without Background
        </button>
      </PopoverContent>
    </Popover>
  );

  if (infographics.length === 1) {
    return (
      <div
        className="slide-container  shadow-lg border rounded-sm w-full max-w-[1280px] px-3 sm:px-12 lg:px-20 py-[10px] sm:py-[40px] lg:py-[86px] font-inter  flex flex-col items-center justify-center max-h-[720px] aspect-video bg-white relative "
        key={infographics[0].chart.chart_type}
        data-slide-element
        data-slide-index={slideIndex}
        data-slide-id={slideId}
        data-slide-type="10"
        data-element-type="slide-container"
        data-element-id={`slide-${slideIndex}-container`}
      >
        <div className="grid grid-cols-2 gap-4 w-full">
          <div className=" flex flex-col w-full items-start justify-center space-y-6">
            <EditableText
              slideIndex={slideIndex}
              elementId={`slide-${slideIndex}-title`}
              type="title"
              content={title}
            />
            {description && (
              <EditableText
                slideIndex={slideIndex}
                elementId={`slide-${slideIndex}-description`}
                type="description"
                content={description}
              />
            )}
          </div>
          <div className="group relative">
            <div className="absolute -inset-[2px] border-2 border-blue-500 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
            {infographics.length < 3 && (
              <button
                onClick={handleAddItem}
                className="absolute top-1/2 -right-4 -translate-y-1/2 p-1 rounded-md bg-white shadow-md opacity-0 group-hover:opacity-100 transition-opacity hover:bg-gray-50 z-50"
              >
                <Plus className="w-4 h-4 text-gray-600" />
              </button>
            )}
            <AllInfoGraphics
              key={infographics[0].chart.chart_type}
              slideIndex={slideIndex}
              itemIndex={0}
              chart={infographics[0].chart}
            />

            <div className="mt-6 text-center w-full">
              <EditableText
                slideIndex={slideIndex}
                elementId={`slide-${slideIndex}-description-body`}
                isAlingCenter={true}
                type="info-description"
                bodyIdx={0}
                content={infographics[0].description}
              />
            </div>
          </div>
        </div>
        <SlideFooter />
      </div>
    );
  } else {
    return (
      <div
        className="slide-container px-3 sm:px-12 lg:px-20 py-[10px] sm:py-[40px] lg:py-[86px] shadow-lg  rounded-sm w-full max-w-[1280px] font-inter  flex flex-col items-center justify-center max-h-[720px] aspect-video bg-white relative"
        data-slide-element
        data-slide-index={slideIndex}
        data-slide-id={slideId}
        data-slide-type="10"
        data-element-type="slide-container"
        data-element-id={`slide-${slideIndex}-container`}
        style={{
          fontFamily: currentColors.fontFamily || "Inter, sans-serif",
        }}
      >
        <div className="text-center space-y-2 lg:space-y-4 mb-3 sm:mb-8 lg:mb-12 w-full">
          <EditableText
            slideIndex={slideIndex}
            elementId={`slide-${slideIndex}-title`}
            type="title"
            isAlingCenter={true}
            content={title}
          />
          {description && (
            <EditableText
              slideIndex={slideIndex}
              elementId={`slide-${slideIndex}-description`}
              type="description"
              isAlingCenter={true}
              content={description}
            />
          )}
        </div>
        <div
          // style={{
          //   gridTemplateColumns: `repeat(${infographics.length}, 1fr)`,
          // }}
          className={`grid w-full  justify-between gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-${infographics.length} lg:gap-6  relative group"`}
        >
          <VariantMenu />
          {/* hover border and icon */}
          <div className="absolute -inset-[2px] border-2 hidden lg:block border-blue-500 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
          {infographics.length < 3 && (
            <button
              onClick={handleAddItem}
              className="absolute top-1/2 -right-4 -translate-y-1/2 p-1 rounded-md bg-white shadow-md opacity-0 group-hover:opacity-100 transition-opacity hover:bg-gray-50 z-50"
            >
              <Plus className="w-4 h-4 text-gray-600" />
            </button>
          )}

          {infographics.map((item: any, index: number) => {
            return (
              <div
                data-slide-element={design_index === 1 ? true : false}
                data-slide-index={slideIndex}
                data-element-type={design_index === 1 ? "slide-box" : ""}
                data-element-id={`slide-${slideIndex}-item-${index}-box`}
                style={{
                  boxShadow:
                    design_index === 1
                      ? "0 2px 10px 0 rgba(43, 43, 43, 0.2)"
                      : "",
                }}
                key={index}
                className={`text-center w-full relative  p-2 lg:px-6 lg:py-8  ${
                  design_index === 1 ? "slide-box rounded-lg " : ""
                }`}
              >
                <ElementMenu
                  index={index}
                  handleDeleteItem={handleDeleteItem}
                />
                <AllInfoGraphics
                  key={item.chart.chart_type}
                  slideIndex={slideIndex}
                  itemIndex={index}
                  chart={item.chart}
                />
                <div className="text-center max-w-md mx-auto  lg:space-y-2">
                  <EditableText
                    slideIndex={slideIndex}
                    bodyIdx={index}
                    elementId={`slide-${slideIndex}-heading-${index}`}
                    type="info-heading"
                    isAlingCenter={true}
                    content={item.title}
                  />
                  <EditableText
                    slideIndex={slideIndex}
                    bodyIdx={index}
                    elementId={`slide-${slideIndex}-description-${index}`}
                    type="info-description"
                    isAlingCenter={true}
                    content={item.description}
                  />
                </div>
              </div>
            );
          })}
        </div>
        <SlideFooter />
      </div>
    );
  }
};

export default Type10Layout;
