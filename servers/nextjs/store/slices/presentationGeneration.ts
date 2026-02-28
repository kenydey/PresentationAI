import { Slide } from "@/app/(presentation-generator)/types/slide";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

<<<<<<< HEAD
export interface PresentationData {
  id: string;
  language: string;
  layout: {
    name: string;
    ordered: boolean;
    slides: any[];
  };
  n_slides: number;
  title: string;
  slides: any;
=======
interface Series {
  data: number[];
  name?: string;
}
interface DataLabel {
  dataLabelPosition: "Outside" | "Inside";
  dataLabelAlignment: "Base" | "Center" | "End";
}
export interface ChartSettings {
  showLegend: boolean;
  showGrid: boolean;
  showAxisLabel: boolean;
  showDataLabel: boolean;
  dataLabel: DataLabel;
}

export interface Chart {
  id: string;
  name: string;
  type: string;
  style: ChartSettings | {} | null;
  unit?: string | null;
  presentation: string;
  postfix: string;
  data: {
    categories: string[];
    series: Series[];
  };
}
export interface PresentationData {
  presentation: {
    created_at: string;
    data: string | null;
    file: string;
    id: string;
    user_id: string;
    n_slides: number;
    prompt: string;
    summary: string | null;
    theme: string | null;
    title: string;
    titles: string[];
    vector_store: string | null;
    thumbnail: string | null;
    language: string;
  } | null;
  slides: Slide[];
>>>>>>> 78e1006 (Initial: presenton)
}

interface PresentationGenerationState {
  presentation_id: string | null;
<<<<<<< HEAD
  isLoading: boolean;
  isStreaming: boolean | null;
  outlines: { content: string }[];
  error: string | null;
  presentationData: PresentationData | null;
  isSlidesRendered: boolean;
  isLayoutLoading: boolean;
=======
  documents: string[];
  images: string[];
  isLoading: boolean;
  isStreaming: boolean | null;
  titles: string[];
  error: string | null;
  presentationData: PresentationData | null;
>>>>>>> 78e1006 (Initial: presenton)
}

const initialState: PresentationGenerationState = {
  presentation_id: null,
<<<<<<< HEAD
  outlines: [],
  isSlidesRendered: false,
  isLayoutLoading: false,
=======
  documents: [],
  images: [],
  titles: [],
>>>>>>> 78e1006 (Initial: presenton)
  isLoading: false,
  isStreaming: null,
  error: null,
  presentationData: null,
};

const presentationGenerationSlice = createSlice({
  name: "presentationGeneration",
  initialState,
  reducers: {
    setStreaming: (state, action: PayloadAction<boolean>) => {
      state.isStreaming = action.payload;
    },
    // Loading
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
<<<<<<< HEAD
    setLayoutLoading: (state, action: PayloadAction<boolean>) => {
      state.isLayoutLoading = action.payload;
    },
=======
>>>>>>> 78e1006 (Initial: presenton)
    // Presentation ID
    setPresentationId: (state, action: PayloadAction<string>) => {
      state.presentation_id = action.payload;
      state.error = null;
    },
<<<<<<< HEAD
    // Slides rendereimport { useEffect } from "react"d
    setSlidesRendered: (state, action: PayloadAction<boolean>) => {
      state.isSlidesRendered = action.payload;
    },
=======
>>>>>>> 78e1006 (Initial: presenton)
    // Error
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.isLoading = false;
    },
    // Clear presentation data
    clearPresentationData: (state) => {
<<<<<<< HEAD
      state.presentationData = null;
    },
    clearOutlines: (state) => {
      state.outlines = [];
    },
    // Set outlines
    setOutlines: (state, action: PayloadAction<{ content: string }[]>) => {
      state.outlines = action.payload;
=======
      state.presentation_id = null;
      state.error = null;
      state.isLoading = false;
    },
    // Set documents
    setDocs: (state, action: PayloadAction<string[]>) => {
      state.documents = action.payload;
    },
    // Set images
    setImgs: (state, action: PayloadAction<string[]>) => {
      state.images = action.payload;
    },
    // Set title with charts
    setTitles: (state, action: PayloadAction<string[]>) => {
      state.titles = action.payload;
>>>>>>> 78e1006 (Initial: presenton)
    },
    // Set presentation data
    setPresentationData: (state, action: PayloadAction<PresentationData>) => {
      state.presentationData = action.payload;
    },
<<<<<<< HEAD
    deleteSlideOutline: (state, action: PayloadAction<{ index: number }>) => {
      if (state.outlines) {
        // Remove the slide at the given index
        state.outlines = state.outlines.filter(
=======
    deleteTitle: (state, action: PayloadAction<{ index: number }>) => {
      if (state.titles) {
        // Remove the slide at the given index
        state.titles = state.titles.filter(
>>>>>>> 78e1006 (Initial: presenton)
          (_, idx) => idx !== action.payload.index
        );
      }
    },
    // SLIDE OPERATIONS
    addSlide: (
      state,
      action: PayloadAction<{ slide: Slide; index: number }>
    ) => {
      if (state.presentationData?.slides) {
        // Insert the new slide at the specified index
        state.presentationData.slides.splice(
          action.payload.index,
          0,
          action.payload.slide
        );

        // Update indices for all slides to ensure they remain sequential
        state.presentationData.slides = state.presentationData.slides.map(
<<<<<<< HEAD
          (slide: any, idx: number) => ({
=======
          (slide, idx) => ({
>>>>>>> 78e1006 (Initial: presenton)
            ...slide,
            index: idx,
          })
        );
      }
    },
    deletePresentationSlide: (state, action: PayloadAction<number>) => {
      if (state.presentationData) {
        state.presentationData.slides.splice(action.payload, 1);
        state.presentationData.slides = state.presentationData.slides.map(
<<<<<<< HEAD
          (slide: any, idx: number) => ({
=======
          (slide, idx) => ({
>>>>>>> 78e1006 (Initial: presenton)
            ...slide,
            index: idx,
          })
        );
      }
    },
    updateSlide: (
      state,
      action: PayloadAction<{ index: number; slide: Slide }>
    ) => {
      if (
        state.presentationData &&
        state.presentationData.slides[action.payload.index]
      ) {
        state.presentationData.slides[action.payload.index] =
          action.payload.slide;
      }
    },
<<<<<<< HEAD

    // Update slide content at specific data path (for Tiptap text editing)
    updateSlideContent: (
      state,
      action: PayloadAction<{
        slideIndex: number;
        dataPath: string;
        content: string;
      }>
    ) => {
      if (
        state.presentationData &&
        state.presentationData.slides &&
        state.presentationData.slides[action.payload.slideIndex]
      ) {
        const slide = state.presentationData.slides[action.payload.slideIndex];
        const { dataPath, content } = action.payload;

        // Helper function to set nested property value
        const setNestedValue = (obj: any, path: string, value: string) => {
          const keys = path.split(/[.\[\]]+/).filter(Boolean);
          let current = obj;

          // Navigate to the parent object
          for (let i = 0; i < keys.length - 1; i++) {
            const key = keys[i];
            if (isNaN(Number(key))) {
              // String key
              if (!current[key]) {
                current[key] = {};
              }
              current = current[key];
            } else {
              // Array index
              const index = Number(key);
              if (!current[index]) {
                current[index] = {};
              }
              current = current[index];
            }
          }

          // Set the final value
          const finalKey = keys[keys.length - 1];
          if (isNaN(Number(finalKey))) {
            current[finalKey] = value;
          } else {
            current[Number(finalKey)] = value;
          }
        };

        // Update the slide content
        if (dataPath && slide.content) {
          setNestedValue(slide.content, dataPath, content);
        }
      }
    },

    addNewSlide: (state, action: PayloadAction<{ slideData: any; index: number }>) => {
      if (state.presentationData?.slides) {
        // Insert the new slide at the specified index + 1 (after current slide)
        state.presentationData.slides.splice(action.payload.index + 1, 0, action.payload.slideData);

        // Update indices for all slides to ensure they remain sequential
        state.presentationData.slides = state.presentationData.slides.map(
          (slide: any, idx: number) => ({
            ...slide,
            index: idx,
          })
        );
      }
    },

    // Update slide image at specific data path
    updateSlideImage: (
      state,
      action: PayloadAction<{
        slideIndex: number;
        dataPath: string;
        imageUrl: string;
        prompt?: string;
      }>
    ) => {
      if (
        state.presentationData &&
        state.presentationData.slides &&
        state.presentationData.slides[action.payload.slideIndex]
      ) {
        const slide = state.presentationData.slides[action.payload.slideIndex];
        const { dataPath, imageUrl, prompt } = action.payload;

        // Helper function to set nested property value for images
        const setNestedImageValue = (obj: any, path: string, url: string, promptText?: string) => {
          const keys = path.split(/[.\[\]]+/).filter(Boolean);
          let current = obj;

          // Navigate to the parent object
          for (let i = 0; i < keys.length - 1; i++) {
            const key = keys[i];
            if (isNaN(Number(key))) {
              if (!current[key]) {
                current[key] = {};
              }
              current = current[key];
            } else {
              const index = Number(key);
              if (!current[index]) {
                current[index] = {};
              }
              current = current[index];
            }
          }

          // Set the image properties
          const finalKey = keys[keys.length - 1];
          const target = isNaN(Number(finalKey)) ? current[finalKey] : current[Number(finalKey)];

          // Preserve existing properties if the target already exists
          const updatedValue = {
            ...(target && typeof target === 'object' ? target : {}),
            __image_url__: url,
            __image_prompt__: promptText || (target?.__image_prompt__) || ''
          };

          if (isNaN(Number(finalKey))) {
            current[finalKey] = updatedValue;
          } else {
            current[Number(finalKey)] = updatedValue;
          }

        };

        // Update the slide image
        if (dataPath && slide.content) {
          setNestedImageValue(slide.content, dataPath, imageUrl, prompt);
        }

        // Also update the images array if it exists
        if (slide.images && Array.isArray(slide.images)) {
          const imageIndex = parseInt(dataPath.split('[')[1]?.split(']')[0]) || 0;
          if (slide.images[imageIndex] !== undefined) {
            slide.images[imageIndex] = imageUrl;
          }
        }
      }
    },

    updateImageProperties: (
      state,
      action: PayloadAction<{
        slideIndex: number;
        itemIndex: number;
        properties: any;
      }>
    ) => {
      if (
        state.presentationData &&
        state.presentationData.slides &&
        state.presentationData.slides[action.payload.slideIndex]
      ) {
        const slide = state.presentationData.slides[action.payload.slideIndex];
        const { itemIndex, properties } = action.payload;
        slide['properties'] = {
          ...slide.properties,
          [itemIndex]: properties
        };

      }
    },

    // Update slide icon at specific data path
    updateSlideIcon: (
      state,
      action: PayloadAction<{
        slideIndex: number;
        dataPath: string;
        iconUrl: string;
        query?: string;
      }>
    ) => {
      if (
        state.presentationData &&
        state.presentationData.slides &&
        state.presentationData.slides[action.payload.slideIndex]
      ) {
        const slide = state.presentationData.slides[action.payload.slideIndex];
        const { dataPath, iconUrl, query } = action.payload;

        // Helper function to set nested property value for icons
        const setNestedIconValue = (obj: any, path: string, url: string, queryText?: string) => {
          const keys = path.split(/[.\[\]]+/).filter(Boolean);
          let current = obj;

          // Navigate to the parent object
          for (let i = 0; i < keys.length - 1; i++) {
            const key = keys[i];
            if (isNaN(Number(key))) {
              if (!current[key]) {
                current[key] = {};
              }
              current = current[key];
            } else {
              const index = Number(key);
              if (!current[index]) {
                current[index] = {};
              }
              current = current[index];
            }
          }

          // Set the icon properties
          const finalKey = keys[keys.length - 1];
          const target = isNaN(Number(finalKey)) ? current[finalKey] : current[Number(finalKey)];

          // Preserve existing properties if the target already exists
          const updatedValue = {
            ...(target && typeof target === 'object' ? target : {}),
            __icon_url__: url,
            __icon_query__: queryText || (target?.__icon_query__) || ''
          };

          if (isNaN(Number(finalKey))) {
            current[finalKey] = updatedValue;
          } else {
            current[Number(finalKey)] = updatedValue;
          }

          // Add debugging
          console.log('Redux: Updated slide icon at path:', path, 'with URL:', url);
        };

        // Update the slide icon
        if (dataPath && slide.content) {
          setNestedIconValue(slide.content, dataPath, iconUrl, query);
        }

        // Also update the icons array if it exists
        if (slide.icons && Array.isArray(slide.icons)) {
          const iconIndex = parseInt(dataPath.split('[')[1]?.split(']')[0]) || 0;
          if (slide.icons[iconIndex] !== undefined) {
            slide.icons[iconIndex] = iconUrl;
          }
        }
=======
    updateSlideVariant: (
      state,
      action: PayloadAction<{ index: number; variant: number }>
    ) => {
      if (
        state.presentationData &&
        state.presentationData.slides[action.payload.index]
      ) {
        state.presentationData.slides[action.payload.index].design_index =
          action.payload.variant;
      }
    },
    updateSlideTitle: (
      state,
      action: PayloadAction<{ index: number; title: string }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]) {
        state.presentationData.slides[action.payload.index].content.title =
          action.payload.title;
      }
    },
    updateSlideDescription: (
      state,
      action: PayloadAction<{ index: number; description: string }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]) {
        state.presentationData.slides[
          action.payload.index
        ].content.description = action.payload.description;
      }
    },
    updateSlideBodyString: (
      state,
      action: PayloadAction<{ index: number; body: string }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]) {
        state.presentationData.slides[action.payload.index].content.body =
          action.payload.body;
      }
    },
    updateSlideBodyHeading: (
      state,
      action: PayloadAction<{ index: number; bodyIdx: number; heading: string }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]) {
        state.presentationData.slides[action.payload.index].content.body[
          action.payload.bodyIdx
          // @ts-ignore
        ].heading = action.payload.heading;
      }
    },
    updateSlideBodyDescription: (
      state,
      action: PayloadAction<{
        index: number;
        bodyIdx: number;
        description: string;
      }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]) {
        state.presentationData.slides[action.payload.index].content.body[
          action.payload.bodyIdx
          // @ts-ignore
        ].description = action.payload.description;
      }
    },
    updateSlideImage: (
      state,
      action: PayloadAction<{ index: number; imageIdx: number; image: string }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]?.images) {
        state.presentationData.slides[action.payload.index].images![
          action.payload.imageIdx
        ] = action.payload.image;
      }
    },
    updateSlideIcon: (
      state,
      action: PayloadAction<{ index: number; iconIdx: number; icon: string }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]?.icons) {
        state.presentationData.slides[action.payload.index].icons![
          action.payload.iconIdx
        ] = action.payload.icon;
      }
    },
    updateSlideChart: (
      state,
      action: PayloadAction<{ index: number; chart: Chart }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]) {
        state.presentationData.slides[action.payload.index].content.graph =
          action.payload.chart;
      }
    },
    updateSlideChartSettings: (
      state,
      action: PayloadAction<{ index: number; chartSettings: ChartSettings }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]) {
        const defaultSettings: ChartSettings = {
          showLegend: false,
          showGrid: false,
          showAxisLabel: true,
          showDataLabel: true,
          dataLabel: {
            dataLabelPosition: "Outside",
            dataLabelAlignment: "Center",
          },
        };
        state.presentationData.slides[
          action.payload.index
        ].content.graph.style = {
          ...defaultSettings,
          ...action.payload.chartSettings,
        };
      }
    },

    addSlideBodyItem: (
      state,
      action: PayloadAction<{
        index: number;
        item: { heading: string; description: string };
      }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]?.content.body) {
        // @ts-ignore
        state.presentationData.slides[action.payload.index].content.body.push(
          action.payload.item
        );
      }
    },
    addSlideImage: (
      state,
      action: PayloadAction<{ index: number; image: string }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]?.images) {
        state.presentationData.slides[action.payload.index].images!.push(
          action.payload.image
        );
      }
    },
    deleteSlideImage: (
      state,
      action: PayloadAction<{ index: number; imageIdx: number }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]?.images) {
        state.presentationData.slides[action.payload.index].images!.splice(
          action.payload.imageIdx,
          1
        );
      }
    },
    updateSlideProperties: (
      state,
      action: PayloadAction<{ index: number; itemIdx: number; properties: any }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]) {
        // Initialize properties object if it doesn't exist
        if (!state.presentationData.slides[action.payload.index].properties) {
          state.presentationData.slides[action.payload.index].properties = {};
        }
        // Assign the properties to the specific item index
        state.presentationData.slides[action.payload.index].properties[
          action.payload.itemIdx
        ] = action.payload.properties;
      }
    },
    // Infographics
    addInfographics: (
      state,
      action: PayloadAction<{ slideIndex: number; item: any }>
    ) => {
      if (state.presentationData?.slides[action.payload.slideIndex]?.content) {
        // @ts-ignore
        state.presentationData.slides[
          action.payload.slideIndex
        ].content.infographics.push(action.payload.item);
      }
    },
    deleteInfographics: (
      state,
      action: PayloadAction<{ slideIndex: number; itemIdx: number }>
    ) => {
      if (state.presentationData?.slides[action.payload.slideIndex]?.content) {
        // @ts-ignore
        state.presentationData.slides[
          action.payload.slideIndex
        ].content.infographics.splice(action.payload.itemIdx, 1);
      }
    },
    updateInfographicsTitle: (
      state,
      action: PayloadAction<{
        slideIndex: number;
        itemIdx: number;
        title: string;
      }>
    ) => {
      if (state.presentationData?.slides[action.payload.slideIndex]?.content) {
        // @ts-ignore
        state.presentationData.slides[
          action.payload.slideIndex
        ].content.infographics[action.payload.itemIdx].title =
          action.payload.title;
      }
    },
    updateInfographicsDescription: (
      state,
      action: PayloadAction<{
        slideIndex: number;
        itemIdx: number;
        description: string;
      }>
    ) => {
      if (state.presentationData?.slides[action.payload.slideIndex]?.content) {
        // @ts-ignore
        state.presentationData.slides[
          action.payload.slideIndex
        ].content.infographics[action.payload.itemIdx].description =
          action.payload.description;
      }
    },
    updateInfographicsChart: (
      state,
      action: PayloadAction<{ slideIndex: number; itemIdx: number; chart: any }>
    ) => {
      if (state.presentationData?.slides[action.payload.slideIndex]?.content) {
        // @ts-ignore
        state.presentationData.slides[
          action.payload.slideIndex
        ].content.infographics[action.payload.itemIdx].chart =
          action.payload.chart;
      }
    },
    deleteSlideBodyItem: (
      state,
      action: PayloadAction<{ index: number; itemIdx: number }>
    ) => {
      if (state.presentationData?.slides[action.payload.index]?.content.body) {
        // @ts-ignore
        state.presentationData.slides[action.payload.index].content.body.splice(
          action.payload.itemIdx,
          1
        );
>>>>>>> 78e1006 (Initial: presenton)
      }
    },
  },
});

export const {
  setStreaming,
  setLoading,
<<<<<<< HEAD
  setLayoutLoading,
  setPresentationId,
  setSlidesRendered,
  setError,
  clearPresentationData,
  clearOutlines,
  deleteSlideOutline,
  setPresentationData,
  setOutlines,
  // slides operations
  addSlide,
  updateSlide,
  deletePresentationSlide,
  updateSlideContent,
  updateSlideImage,
  updateImageProperties,
  updateSlideIcon,
  addNewSlide,
=======
  setPresentationId,
  setError,
  clearPresentationData,
  setDocs,
  setImgs,

  deleteTitle,
  setPresentationData,
  setTitles,
  // slides operations
  addSlide,
  updateSlide,
  updateSlideVariant,
  updateSlideChart,
  updateSlideChartSettings,
  updateSlideTitle,
  updateSlideDescription,
  updateSlideBodyString,
  updateSlideBodyHeading,
  updateSlideBodyDescription,
  updateSlideImage,
  updateSlideIcon,
  deletePresentationSlide,
  addSlideBodyItem,
  addSlideImage,
  deleteSlideImage,
  deleteSlideBodyItem,
  updateSlideProperties,
  // infographics
  addInfographics,
  deleteInfographics,
  updateInfographicsTitle,
  updateInfographicsDescription,
  updateInfographicsChart,
>>>>>>> 78e1006 (Initial: presenton)
} = presentationGenerationSlice.actions;

export default presentationGenerationSlice.reducer;
