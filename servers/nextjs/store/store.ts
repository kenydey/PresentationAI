import { configureStore } from "@reduxjs/toolkit";

import presentationGenerationReducer from "./slices/presentationGeneration";
<<<<<<< HEAD
import pptGenUploadReducer from "./slices/presentationGenUpload";
import userConfigReducer from "./slices/userConfig";
import undoRedoReducer from "./slices/undoRedoSlice";
export const store = configureStore({
  reducer: {
    presentationGeneration: presentationGenerationReducer,
    pptGenUpload: pptGenUploadReducer,
    userConfig: userConfigReducer,
    undoRedo: undoRedoReducer,
=======
import themeReducer from "@/app/(presentation-generator)/store/themeSlice";
import pptGenUploadSlice from "./slices/presentationGenUpload";
export const store = configureStore({
  reducer: {
    presentationGeneration: presentationGenerationReducer,
    theme: themeReducer,
    pptGenUpload: pptGenUploadSlice,
>>>>>>> 78e1006 (Initial: presenton)
  },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
