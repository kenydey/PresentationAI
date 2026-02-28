import { getHeader, getHeaderForFormData } from "./header";
<<<<<<< HEAD
import { IconSearch, ImageGenerate, ImageSearch, PreviousGeneratedImagesResponse } from "./params";
import { ApiResponseHandler } from "./api-error-handler";

export class PresentationGenerationApi {
  static async uploadDoc(documents: File[]) {
    const formData = new FormData();

    documents.forEach((document) => {
      formData.append("files", document);
=======
import { IconSearch, ImageGenerate, ImageSearch } from "./params";

export class PresentationGenerationApi {
  // static BASE_URL="https://api.presenton.ai";
  // static BASE_URL="https://presentation-generator-fragrant-mountain-1643.fly.dev";
  static BASE_URL = process.env.NEXT_PUBLIC_API || 'http://localhost:8000';
  // static BASE_URL = "http://localhost:48388";

  static async getChapterDetails() {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/chapter-details`,
        {
          method: "GET",
          headers: getHeader(),
          cache: "no-cache",
        }
      );
      if (response.status === 200) {
        const data = await response.json();
        return data;
      }
    } catch (error) {
      console.error("Error getting chapter details:", error);
      throw error;
    }
  }

  static async uploadDoc(documents: File[], images: File[]) {
    const formData = new FormData();

    documents.forEach((document) => {
      formData.append("documents", document);
    });

    images.forEach((image) => {
      formData.append("images", image);
>>>>>>> 78e1006 (Initial: presenton)
    });

    try {
      const response = await fetch(
<<<<<<< HEAD
        `/api/v1/ppt/files/upload`,
        {
          method: "POST",
          headers: getHeaderForFormData(),
=======
        `${PresentationGenerationApi.BASE_URL}/ppt/files/upload`,
        {
          method: "POST",
          headers: getHeaderForFormData(),
          // Remove Content-Type header as browser will set it automatically with boundary
>>>>>>> 78e1006 (Initial: presenton)
          body: formData,
          cache: "no-cache",
        }
      );

<<<<<<< HEAD
      return await ApiResponseHandler.handleResponse(response, "Failed to upload documents");
=======
      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const data = await response.json();
      return data;
>>>>>>> 78e1006 (Initial: presenton)
    } catch (error) {
      console.error("Upload error:", error);
      throw error;
    }
  }

<<<<<<< HEAD
  static async decomposeDocuments(documentKeys: string[]) {
    try {
      const response = await fetch(
        `/api/v1/ppt/files/decompose`,
=======
  static async generateResearchReport(prompt: string, language: string | null) {
    const apiBody = {
      query: prompt,
      language: language,
    };
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/report/generate`,
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify(apiBody),
          cache: "no-cache",
        }
      );

      if (response.status === 200) {
        const data = await response.json();

        return data;
      } else {
        throw new Error(`Failed to generate report: ${response.statusText}`);
      }
    } catch (error) {
      console.error("Error in Generate Research Report", error);
      throw error;
    }
  }

  static async decomposeDocuments(documentKeys: string[], imageKeys: string[]) {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/files/decompose`,
>>>>>>> 78e1006 (Initial: presenton)
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify({
<<<<<<< HEAD
            file_paths: documentKeys,
=======
            documents: documentKeys,
            images: imageKeys,
>>>>>>> 78e1006 (Initial: presenton)
          }),
          cache: "no-cache",
        }
      );
<<<<<<< HEAD
      
      return await ApiResponseHandler.handleResponse(response, "Failed to decompose documents");
=======
      if (response.status === 200) {
        const data = await response.json();

        return data;
      } else {
        throw new Error(`Failed to decompose files: ${response.statusText}`);
      }
>>>>>>> 78e1006 (Initial: presenton)
    } catch (error) {
      console.error("Error in Decompose Files", error);
      throw error;
    }
  }
<<<<<<< HEAD
 
   static async createPresentation({
    content,
    n_slides,
    file_paths,
    language,
    tone,
    verbosity,
    instructions,
    include_table_of_contents,
    include_title_slide,
    web_search,
    
  }: {
    content: string;
    n_slides: number | null;
    file_paths?: string[];
    language: string | null;
    tone?: string | null;
    verbosity?: string | null;
    instructions?: string | null;
    include_table_of_contents?: boolean;
    include_title_slide?: boolean;
    web_search?: boolean;
  }) {
    try {
      const response = await fetch(
        `/api/v1/ppt/presentation/create`,
=======
  static async titleGeneration({
    presentation_id,
  }: {
    presentation_id: string;
  }) {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/titles/generate`,
>>>>>>> 78e1006 (Initial: presenton)
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify({
<<<<<<< HEAD
            content,
            n_slides,
            file_paths,
            language,
            tone,
            verbosity,
            instructions,
            include_table_of_contents,
            include_title_slide,
            web_search,
=======
            prompt: prompt,
            presentation_id: presentation_id,
>>>>>>> 78e1006 (Initial: presenton)
          }),
          cache: "no-cache",
        }
      );
<<<<<<< HEAD
      
      return await ApiResponseHandler.handleResponse(response, "Failed to create presentation");
    } catch (error) {
      console.error("error in presentation creation", error);
=======
      if (response.status === 200) {
        const data = await response.json();

        return data;
      } else {
        throw new Error(`Failed to generate titles: ${response.statusText}`);
      }
    } catch (error) {
      console.error("error in title generation", error);
>>>>>>> 78e1006 (Initial: presenton)
      throw error;
    }
  }

<<<<<<< HEAD
  static async editSlide(
    slide_id: string,
=======
  static async generatePresentation(presentationData: any) {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/generate`,
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify(presentationData),
          cache: "no-cache",
        }
      );
      if (response.status === 200) {
        const data = await response.json();

        return data;
      } else {
        throw new Error(
          `Failed to generate presentation: ${response.statusText}`
        );
      }
    } catch (error) {
      console.error("error in presentation generation", error);
      throw error;
    }
  }
  static async editSlide(
    presentation_id: string,
    index: number,
>>>>>>> 78e1006 (Initial: presenton)
    prompt: string
  ) {
    try {
      const response = await fetch(
<<<<<<< HEAD
        `/api/v1/ppt/slide/edit`,
=======
        `${PresentationGenerationApi.BASE_URL}/ppt/edit`,
>>>>>>> 78e1006 (Initial: presenton)
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify({
<<<<<<< HEAD
            id: slide_id,
=======
            presentation_id,

            index,
>>>>>>> 78e1006 (Initial: presenton)
            prompt,
          }),
          cache: "no-cache",
        }
      );

<<<<<<< HEAD
      return await ApiResponseHandler.handleResponse(response, "Failed to update slide");
=======
      if (!response.ok) {
        throw new Error("Failed to update slides");
      }

      const data = await response.json();
      return data;
>>>>>>> 78e1006 (Initial: presenton)
    } catch (error) {
      console.error("error in slide update", error);
      throw error;
    }
  }

  static async updatePresentationContent(body: any) {
    try {
      const response = await fetch(
<<<<<<< HEAD
        `/api/v1/ppt/presentation/update`,
        {
          method: "PATCH",
=======
        `${PresentationGenerationApi.BASE_URL}/ppt/slides/update`,
        {
          method: "POST",
>>>>>>> 78e1006 (Initial: presenton)
          headers: getHeader(),
          body: JSON.stringify(body),
          cache: "no-cache",
        }
      );
<<<<<<< HEAD
      
      return await ApiResponseHandler.handleResponse(response, "Failed to update presentation content");
=======
      if (response.ok) {
        const data = await response.json();

        return data;
      } else {
        throw new Error(
          `Failed to update presentation content: ${response.statusText}`
        );
      }
>>>>>>> 78e1006 (Initial: presenton)
    } catch (error) {
      console.error("error in presentation content update", error);
      throw error;
    }
  }

<<<<<<< HEAD
  static async presentationPrepare(presentationData: any) {
    try {
      const response = await fetch(
        `/api/v1/ppt/presentation/prepare`,
=======
  static async generateData(presentationData: any) {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/generate/data`,
>>>>>>> 78e1006 (Initial: presenton)
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify(presentationData),
          cache: "no-cache",
        }
      );
<<<<<<< HEAD
      
      return await ApiResponseHandler.handleResponse(response, "Failed to prepare presentation");
=======
      if (response.ok) {
        const data = await response.json();

        return data;
      } else {
        throw new Error(`Failed to generate data: ${response.statusText}`);
      }
>>>>>>> 78e1006 (Initial: presenton)
    } catch (error) {
      console.error("error in data generation", error);
      throw error;
    }
  }
<<<<<<< HEAD
  
  // IMAGE AND ICON SEARCH
  
  
  static async generateImage(imageGenerate: ImageGenerate) {
    try {
      const response = await fetch(
        `/api/v1/ppt/images/generate?prompt=${imageGenerate.prompt}`,
        {
          method: "GET",
          headers: getHeader(),
          cache: "no-cache",
        }
      );
      
      return await ApiResponseHandler.handleResponse(response, "Failed to generate image");
=======
  // IMAGE AND ICON SEARCH
  static async imageSearch(imageSearch: ImageSearch) {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/image/search`,
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify(imageSearch),
          cache: "no-cache",
        }
      );
      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        throw new Error(`Failed to search images: ${response.statusText}`);
      }
    } catch (error) {
      console.error("error in image search", error);
      throw error;
    }
  }
  static async generateImage(imageGenerate: ImageGenerate) {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/image/generate`,
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify(imageGenerate),
          cache: "no-cache",
        }
      );
      if (response.ok) {
        const data = await response.json();

        return data;
      } else {
        throw new Error(`Failed to generate images: ${response.statusText}`);
      }
>>>>>>> 78e1006 (Initial: presenton)
    } catch (error) {
      console.error("error in image generation", error);
      throw error;
    }
  }
<<<<<<< HEAD

  static getPreviousGeneratedImages = async (): Promise<PreviousGeneratedImagesResponse[]> => {
    try {
      const response = await fetch(
        `/api/v1/ppt/images/generated`,
        {
          method: "GET",
          headers: getHeader(),
        }
      );
      
      return await ApiResponseHandler.handleResponse(response, "Failed to get previous generated images");
    } catch (error) {
      console.error("error in getting previous generated images", error);
      throw error;
    }
  }
  
  static async searchIcons(iconSearch: IconSearch) {
    try {
      const response = await fetch(
        `/api/v1/ppt/icons/search?query=${iconSearch.query}&limit=${iconSearch.limit}`,
        {
          method: "GET",
          headers: getHeader(),
          cache: "no-cache",
        }
      );
      
      return await ApiResponseHandler.handleResponse(response, "Failed to search icons");
=======
  static async searchIcons(iconSearch: IconSearch) {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/icon/search`,
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify(iconSearch),
          cache: "no-cache",
        }
      );
      if (response.ok) {
        const data = await response.json();

        return data;
      } else {
        throw new Error(`Failed to search icons: ${response.statusText}`);
      }
>>>>>>> 78e1006 (Initial: presenton)
    } catch (error) {
      console.error("error in icon search", error);
      throw error;
    }
  }

<<<<<<< HEAD

=======
  static async updateDocuments(body: any) {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/document/update`,
        {
          method: "POST",
          headers: getHeaderForFormData(),
          body: body,
          cache: "no-cache",
        }
      );
      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        throw new Error(`Failed to update documents: ${response.statusText}`);
      }
    } catch (error) {
      console.error("error in document update", error);
      throw error;
    }
  }
>>>>>>> 78e1006 (Initial: presenton)

  // EXPORT PRESENTATION
  static async exportAsPPTX(presentationData: any) {
    try {
      const response = await fetch(
<<<<<<< HEAD
        `/api/v1/ppt/presentation/export/pptx`,
=======
        `${PresentationGenerationApi.BASE_URL}/ppt/presentation/export_as_pptx/`,
>>>>>>> 78e1006 (Initial: presenton)
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify(presentationData),
          cache: "no-cache",
        }
      );
<<<<<<< HEAD
      return await ApiResponseHandler.handleResponse(response, "Failed to export as PowerPoint");
=======
      if (response.ok) {
        const data = await response.json();

        return {
          ...data,
          url: `${PresentationGenerationApi.BASE_URL}${data.url}`,
        };
      } else {
        throw new Error(`Failed to export as pptx: ${response.statusText}`);
      }
>>>>>>> 78e1006 (Initial: presenton)
    } catch (error) {
      console.error("error in pptx export", error);
      throw error;
    }
  }
<<<<<<< HEAD
  
  

}
=======
  static async exportAsPDF(presentationData: any) {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/presentation/export_as_pdf/`,
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify(presentationData),
        }
      );
      if (response.ok) {
        const data = await response.json();

        return data;
      } else {
        throw new Error(`Failed to export as pdf: ${response.statusText}`);
      }
    } catch (error) {
      console.error("error in pdf export", error);
      throw error;
    }
  }
  static async deleteSlide(presentation_id: string, slide_id: string) {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/slide/delete?presentation_id=${presentation_id}&slide_id=${slide_id}`,
        {
          method: "DELETE",
          headers: getHeader(),
          cache: "no-cache",
        }
      );
      if (response.status === 204) {
        return true;
      } else {
        throw new Error(`Failed to delete slide: ${response.statusText}`);
      }
    } catch (error) {
      console.error("error in slide deletion", error);
      throw error;
    }
  }
  // SET THEME COLORS
  static async setThemeColors(presentation_id: string, theme: any) {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/presentation/theme`,
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify({
            presentation_id,
            theme,
          }),
         
        }
      );
      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        throw new Error(`Failed to set theme colors: ${response.statusText}`);
      }
    } catch (error) {
      console.error("error in theme colors set", error);
      throw error;
    }
  }
  // QUESTIONS

  static async getQuestions({
    prompt,
    n_slides,
    documents,
    images,
    research_reports,
    language,
    sources,
  }: {
    prompt: string;
    n_slides: number | null;
    documents?: string[];
    images?: string[];
    research_reports?: string[];
    language: string | null;
    sources?: string[];
  }) {
    try {
      const response = await fetch(
        `${PresentationGenerationApi.BASE_URL}/ppt/create`,
        {
          method: "POST",
          headers: getHeader(),
          body: JSON.stringify({
            prompt,
            n_slides,
            language,
            documents,
            research_reports,
            images,
            sources,
          }),
          cache: "no-cache",
        }
      );
      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        throw new Error(`Failed to get questions: ${response.statusText}`);
      }
    } catch (error) {
      console.error("error in question generation", error);
      throw error;
    }
  }
}
>>>>>>> 78e1006 (Initial: presenton)
