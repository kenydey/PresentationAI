import {
  updateSlideDescription,
  updateSlideBodyString,
  updateSlideTitle,
  updateSlideBodyHeading,
  updateSlideBodyDescription,
} from "@/store/slices/presentationGeneration";
import React, { useCallback, useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import TipTapEditor from "./Tiptap";
import { RootState } from "@/store/store";
import Typewriter from "./TypeWriter";
import MarkdownRenderer from "../documents-preview/components/MarkdownRenderer";

interface EditableTextProps {
  slideIndex: number;
  bodyIdx?: number;
  elementId: string; // Format: 'title' | 'body.0.heading' | 'body.0.description'
  type:
    | "title"
    | "heading"
    | "description-body"
    | "description"
    | "heading-description"
    | "info-heading"
    | "info-description";
  content: string;
  isAlingCenter?: boolean;
}

const EditableText = ({
  slideIndex,
  elementId,
  type,
  content,
  bodyIdx = 0,
  isAlingCenter = false,
}: EditableTextProps) => {
  const dispatch = useDispatch();
  const { isStreaming } = useSelector(
    (state: RootState) => state.presentationGeneration
  );

  const elementRef = useRef<HTMLDivElement>(null);

  // Add useEffect to initialize content
  useEffect(() => {
    if (elementRef.current) {
      const displayContent = content || getPlaceholder();
      elementRef.current.textContent = displayContent;

      // Add placeholder styling if needed
      if (!content) {
        elementRef.current.classList.add("text-gray-400");
      }
    }
  }, [content]);

  const getPlaceholder = () => {
    switch (type) {
      case "title":
        return "Enter title";
      case "heading":
        return "Enter heading";
      case "description-body":
        return "Enter description";
      case "description":
        return "Enter description";
      case "heading-description":
        return "Enter description";
      case "info-heading":
        return "Enter heading";
      case "info-description":
        return "Enter description";
      default:
        return "Enter text";
    }
  };

  const handleInput = useCallback((event: React.FormEvent<HTMLDivElement>) => {
    const element = event.currentTarget;
    const newContent = element.textContent || "";

    // Handle placeholder text
    if (newContent === getPlaceholder()) {
      element.classList.add("text-gray-400");
    } else {
      element.classList.remove("text-gray-400");
    }
  }, []);

  const handleFocus = (event: React.FocusEvent<HTMLDivElement>) => {
    const element = event.currentTarget;
    if (element.textContent === getPlaceholder()) {
      element.textContent = "";
      element.classList.remove("text-gray-400");
    }
  };

  const handleBlur = (event: React.FocusEvent<HTMLDivElement>) => {
    const element = event.currentTarget;
    const newContent = element.textContent?.trim() || "";

    if (!newContent) {
      element.textContent = getPlaceholder();
      element.classList.add("text-gray-400");
    }
    updateSlide(type, newContent);
  };
  const updateSlide = (type: string, value: string) => {
    switch (type) {
      case "title":
        dispatch(updateSlideTitle({ index: slideIndex, title: value }));
        break;
      case "heading":
        dispatch(
          updateSlideBodyHeading({
            index: slideIndex,
            bodyIdx: bodyIdx,
            heading: value,
          })
        );
        break;
      case "description":
        dispatch(
          updateSlideDescription({ index: slideIndex, description: value })
        );
        break;
      case "heading-description":
        dispatch(
          updateSlideBodyDescription({
            index: slideIndex,
            bodyIdx: bodyIdx,
            description: value,
          })
        );
        break;
      case "description-body":
        dispatch(updateSlideBodyString({ index: slideIndex, body: value }));
        break;
    }
  };

  const getTextStyle = () => {
    const baseStyle = "outline-none  transition-all duration-200";
    switch (type) {
      case "title":
        return `${baseStyle} text-[40px] slide-title leading-[48px] font-bold`;
      case "heading":
        return `${baseStyle} text-[24px] slide-heading leading-[32px] font-bold`;
      case "description":
      case "description-body":
      case "heading-description":
        return `${baseStyle} text-[20px] slide-description leading-[24px] font-normal`;
      default:
        return `${baseStyle} text-[20px] slide-description leading-[24px] font-normal`;
    }
  };

  return (
    <>
      {isStreaming ? (
        <div
          className={`w-full  min-w-[60px]  font-inter ${getTextStyle()}  ${
            isAlingCenter ? "text-center " : ""
          }`}
        >
          <Typewriter text={content.replace(/\*\*/g, "")} speed={20} />
        </div>
      ) : (
        <TipTapEditor
          key={content}
          bodyIdx={bodyIdx}
          isAlingCenter={isAlingCenter}
          slideIndex={slideIndex}
          elementId={elementId}
          type={type}
          content={content}
        />
      )}
    </>
  );
};

export default React.memo(EditableText);
