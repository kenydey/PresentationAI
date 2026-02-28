import { PresentationConfig } from "@/app/(presentation-generator)/upload/type";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface PresentationGenUploadState {
  config: PresentationConfig | null;
<<<<<<< HEAD
  
  files: any;

=======
  reports: any;
  documents: any;
  images: any;
  charts: any;
  tables: any;
  questions: any;
  storyResponse: any;
>>>>>>> 78e1006 (Initial: presenton)
}

const initialState: PresentationGenUploadState = {
  config: null,
<<<<<<< HEAD
  files: [],
=======
  reports: {},
  documents: {},
  images: {},
  charts: {},
  tables: {},

  questions: [],
  storyResponse: {
    big_idea: null,
    story_type: null,
    story: null,
  },
>>>>>>> 78e1006 (Initial: presenton)
};

export const presentationGenUploadSlice = createSlice({
  name: "pptGenUpload",
  initialState,
  reducers: {
    setPptGenUploadState: (
      state,
      action: PayloadAction<Partial<PresentationGenUploadState>>
    ) => {
      const payload = action.payload;
      state.config = payload.config!;
<<<<<<< HEAD
      state.files = payload.files!;
    },
   
  },
});

export const { setPptGenUploadState, } =
=======
      state.reports = payload.reports;
      state.documents = payload.documents;
      state.images = payload.images;
      state.charts = payload.charts;
      state.tables = payload.tables;

      state.questions = payload.questions;
    },
    setQuestions: (state, action: PayloadAction<any>) => {
      state.questions = action.payload;
    },
    setStoryResponse: (state, action: PayloadAction<any>) => {
      state.storyResponse = action.payload;
    },
  },
});

export const { setPptGenUploadState, setQuestions, setStoryResponse } =
>>>>>>> 78e1006 (Initial: presenton)
  presentationGenUploadSlice.actions;
export default presentationGenUploadSlice.reducer;
