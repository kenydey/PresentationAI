export interface ImageSearch {
  presentation_id: string;
  query: string;
  page: number;
  limit: number;
}

export interface ImageGenerate {
<<<<<<< HEAD
  

  prompt: string;
}
export interface IconSearch {
 

  query: string;

  limit: number;
}

export interface PreviousGeneratedImagesResponse {

    extras: {
      prompt: string;
      theme_prompt: string | null;
    },
    created_at: string;
    id: string;
    path: string;
}
=======
  presentation_id: string;
  prompt: {
    theme_prompt: string;
    image_prompt: string;
    aspect_ratio: string;
  };
}
export interface IconSearch {
  presentation_id: string;

  query: string;
  category?: string;
  page: number;
  limit: number;
}
>>>>>>> 78e1006 (Initial: presenton)
