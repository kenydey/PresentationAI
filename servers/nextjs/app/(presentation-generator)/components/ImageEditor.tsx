"use client";
import React, { useEffect, useState, useRef } from "react";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
<<<<<<< HEAD
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Wand2, Upload, Loader2, Delete, Trash } from "lucide-react";
import { cn } from "@/lib/utils";
import { PresentationGenerationApi } from "../services/api/presentation-generation";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import { PreviousGeneratedImagesResponse } from "../services/api/params";
import { trackEvent, MixpanelEvent } from "@/utils/mixpanel";
import { ImagesApi } from "../services/api/images";
import { ImageAssetResponse } from "../services/api/types";
interface ImageEditorProps {
  initialImage: string | null;
  imageIdx?: number;
  slideIndex: number;
  className?: string;
  promptContent?: string;
  properties?: null | any;
  onClose?: () => void;
  onImageChange?: (newImageUrl: string, prompt?: string) => void;
  onFocusPointClick?: (propertiesData: any) => void;
=======
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Search,
  Wand2,
  Upload,
  Edit,
  Crop,
  Move,
  Maximize,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useDispatch, useSelector } from "react-redux";
import { PresentationGenerationApi } from "../services/api/presentation-generation";
import { RootState } from "@/store/store";
import { usePathname } from "next/navigation";
import { Skeleton } from "@/components/ui/skeleton";
import {
  updateSlideImage,
  updateSlideProperties,
} from "@/store/slices/presentationGeneration";
import { ThemeImagePrompt } from "../utils/others";

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import ToolTip from "@/components/ToolTip";

interface ImageEditorProps {
  initialImage: string | null;
  imageIdx?: number;
  title: string;
  slideIndex: number;
  elementId: string;
  className?: string;
  promptContent?: string;
  properties?: null | any;
>>>>>>> 78e1006 (Initial: presenton)
}

const ImageEditor = ({
  initialImage,
  imageIdx = 0,
<<<<<<< HEAD
  promptContent,
  properties,
  onClose,
  onFocusPointClick,
  onImageChange,
}: ImageEditorProps) => {
  // State management
  const [previewImages, setPreviewImages] = useState(initialImage);
  const [previousGeneratedImages, setPreviousGeneratedImages] = useState<
    PreviousGeneratedImagesResponse[]
  >([]);
  const [prompt, setPrompt] = useState<string>("");
  const [isGenerating, setIsGenerating] = useState(false);
=======
  className,
  title,
  slideIndex,
  elementId,
  promptContent,
  properties,
}: ImageEditorProps) => {
  const dispatch = useDispatch();

  const { currentTheme } = useSelector((state: RootState) => state.theme);

  const path = usePathname();
  const [image, setImage] = useState(initialImage);
  const [previewImages, setPreviewImages] = useState([initialImage]);
  const [searchedImages, setSearchedImages] = useState<string[]>([]);
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [isToolbarOpen, setIsToolbarOpen] = useState(false);
  const [prompt, setPrompt] = useState<string>("");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
>>>>>>> 78e1006 (Initial: presenton)
  const [error, setError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [uploadedImageUrl, setUploadedImageUrl] = useState<string | null>(null);
<<<<<<< HEAD
  const [isOpen, setIsOpen] = useState(true);
  const [uploadedImages, setUploadedImages] = useState<ImageAssetResponse[]>([]);
  const [uploadedImagesLoading, setUploadedImagesLoading] = useState(false);
  // Focus point and object fit for image editing
=======
>>>>>>> 78e1006 (Initial: presenton)
  const [isFocusPointMode, setIsFocusPointMode] = useState(false);
  const [focusPoint, setFocusPoint] = useState(
    (properties &&
      properties[imageIdx] &&
      properties[imageIdx].initialFocusPoint) || {
      x: 50,
      y: 50,
    }
  );
  const [objectFit, setObjectFit] = useState<"cover" | "contain" | "fill">(
    (properties &&
      properties[imageIdx] &&
      properties[imageIdx].initialObjectFit) ||
      "cover"
  );
<<<<<<< HEAD

  // Refs
  const imageRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    setPreviewImages(initialImage);
  }, [initialImage]);

  useEffect(() => {
    if (isOpen && !previousGeneratedImages.length) {
      getPreviousGeneratedImage();
    }
  }, [isOpen]);

  // Handle close with animation
  const handleClose = () => {

    setIsOpen(false);
    // Delay the actual close to allow animation to complete
    setTimeout(() => {
      onClose?.();
    }, 300); // Match the Sheet animation duration
  };

  const getPreviousGeneratedImage = async () => {
    try {
      trackEvent(MixpanelEvent.ImageEditor_GetPreviousGeneratedImages_API_Call);
      const response =
        await PresentationGenerationApi.getPreviousGeneratedImages();
      setPreviousGeneratedImages(response);
    } catch (error: any) {
      toast.error("Failed to get previous generated images. Please try again.");
      console.error("error in getting previous generated images", error);
      setError(
        error.message ||
          "Failed to get previous generated images. Please try again."
      );
    }
  };

  /**
   * Handles image selection and calls the parent callback
   */
  const handleImageChange = (newImage: string) => {
    if (onImageChange) {
      onImageChange(newImage, promptContent);
      setPreviewImages(newImage);
    }
  };

  /**
   * Handles focus point adjustment when clicking on the image
   */
=======
  const imageRef = useRef<HTMLImageElement>(null);
  const imageContainerRef = useRef<HTMLDivElement>(null);
  const toolbarRef = useRef<HTMLDivElement>(null);
  const popoverContentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setImage(initialImage);
    setPreviewImages([initialImage]);
  }, [initialImage]);

  // Close toolbar when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        imageContainerRef.current &&
        !imageContainerRef.current.contains(event.target as Node) &&
        toolbarRef.current &&
        !toolbarRef.current.contains(event.target as Node) &&
        !popoverContentRef.current
      ) {
        setIsToolbarOpen(false);
        if (isFocusPointMode) {
          // saveFocusPoint(); // Save focus point before closing
          saveImageProperties(objectFit, focusPoint);
        }
        setIsFocusPointMode(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isFocusPointMode, focusPoint]);

  const handleImageClick = () => {
    if (!isFocusPointMode) {
      setIsToolbarOpen(true);
    }
  };

  const handleOpenEditor = () => {
    setIsToolbarOpen(false);
    setIsEditorOpen(true);
  };

  const handleImageChange = (newImage: string) => {
    setImage(newImage);
    dispatch(
      updateSlideImage({
        index: slideIndex,
        imageIdx: imageIdx,
        image: newImage,
      })
    );
    setIsEditorOpen(false);
  };

>>>>>>> 78e1006 (Initial: presenton)
  const handleFocusPointClick = (e: React.MouseEvent) => {
    if (!isFocusPointMode || !imageRef.current) return;

    const rect = imageRef.current.getBoundingClientRect();
    const x = Math.max(
      0,
      Math.min(100, ((e.clientX - rect.left) / rect.width) * 100)
    );
    const y = Math.max(
      0,
      Math.min(100, ((e.clientY - rect.top) / rect.height) * 100)
    );

    setFocusPoint({ x, y });
    saveImageProperties(objectFit, { x, y });

    // Apply the focus point in real-time
    if (imageRef.current) {
      imageRef.current.style.objectPosition = `${x}% ${y}%`;
    }
  };

<<<<<<< HEAD
  /**
   * Toggles focus point adjustment mode
   */
  const toggleFocusPointMode = () => {
    if (isFocusPointMode) {
      saveImageProperties(objectFit, focusPoint);
=======
  const toggleFocusPointMode = () => {
    if (isFocusPointMode) {
      // If turning off focus point mode, save the current focus point
      // saveFocusPoint();
>>>>>>> 78e1006 (Initial: presenton)
    }
    setIsFocusPointMode(!isFocusPointMode);
  };

<<<<<<< HEAD
  /**
   * Handles object fit change
   */
=======
>>>>>>> 78e1006 (Initial: presenton)
  const handleFitChange = (fit: "cover" | "contain" | "fill") => {
    setObjectFit(fit);

    if (imageRef.current) {
      imageRef.current.style.objectFit = fit;
    }

<<<<<<< HEAD
    saveImageProperties(fit, focusPoint);
  };

  /**
   * Saves image properties (focus point and object fit)
   */
=======
    // Save the fit change to your state
    saveImageProperties(fit, focusPoint);
  };

>>>>>>> 78e1006 (Initial: presenton)
  const saveImageProperties = (
    fit: "cover" | "contain" | "fill",
    focusPoint: { x: number; y: number }
  ) => {
    const propertiesData = {
      initialObjectFit: fit,
      initialFocusPoint: focusPoint,
    };
<<<<<<< HEAD
    // TODO: Save to Redux store if needed
    onFocusPointClick?.(propertiesData);
  };

  /**
   * Generates new images using AI
   */
  const handleGenerateImage = async () => {
    if (!prompt) {
      setError("Please enter a prompt");
      return;
    }
    try {
      setIsGenerating(true);
      setError(null);
      trackEvent(MixpanelEvent.ImageEditor_GenerateImage_API_Call);
      const response = await PresentationGenerationApi.generateImage({
        prompt: prompt,
      });

      setPreviewImages(response);
    } catch (err: any) {
      console.error("Error in image generation", err);
      setError(err.message || "Failed to generate image. Please try again.");
=======

    dispatch(
      updateSlideProperties({
        index: slideIndex,
        itemIdx: imageIdx,
        properties: propertiesData,
      })
    );
  };

  const handleGenerateImage = async () => {
    try {
      setIsGenerating(true);
      setError(null);

      const presentation_id = path.split("/")[2];

      const response = await PresentationGenerationApi.generateImage({
        presentation_id,
        prompt: {
          theme_prompt: ThemeImagePrompt[currentTheme],
          image_prompt: prompt,
          aspect_ratio: "4:5",
        },
      });

      setPreviewImages(response.urls);
    } catch (err) {
      setError("Failed to generate image. Please try again.");
>>>>>>> 78e1006 (Initial: presenton)
    } finally {
      setIsGenerating(false);
    }
  };

<<<<<<< HEAD
  /**
   * Handles file upload
   */
  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file size (5MB limit)
    if (file.size > 5 * 1024 * 1024) {
      setUploadError("File size should be less than 5MB");
      return;
    }

    // Validate file type
    if (!file.type.startsWith("image/")) {
      setUploadError("Please upload an image file");
      return;
    }
    try {
      setIsUploading(true);
      setUploadError(null);
      trackEvent(MixpanelEvent.ImageEditor_UploadImage_API_Call);
      const result = await ImagesApi.uploadImage(file);
      setUploadedImageUrl(result.path);
    } catch (err:any) {
      setUploadError("Failed to upload image. Please try again.");
      toast.error(err.message || "Failed to upload image. Please try again.");
      console.log("Upload error:", err.message);
=======
  const handleSearchImage = async () => {
    const presentation_id = path.split("/")[2];

    try {
      setIsSearching(true);
      setError(null);

      const response = await PresentationGenerationApi.imageSearch({
        presentation_id: presentation_id,
        query: searchQuery,
        page: 1,
        limit: 20,
      });

      setSearchedImages(response.urls);
    } catch (err) {
      setError("Failed to fetch images. Please try again.");
    } finally {
      setIsSearching(false);
    }
  };

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const presentation_id = path.split("/")[2];
    const file = event.target.files?.[0];
    if (!file) return;

    // Check file size (e.g., 5MB limit)
    if (file.size > 5 * 1024 * 1024) {
      const error_message = "File size should be less than 5MB";

      setUploadError(error_message);
      return;
    }

    // Check file type
    if (!file.type.startsWith("image/")) {
      const error_message = "Please upload an image file";

      setUploadError(error_message);
      return;
    }

    try {
      setIsUploading(true);
      setUploadError(null);

      const formData = new FormData();
      formData.append("file", file);
      const response = await fetch("/api/user-upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();
      setUploadedImageUrl(data.url);
    } catch (err) {
      const error_message = "Failed to upload image. Please try again.";

      setUploadError(error_message);
>>>>>>> 78e1006 (Initial: presenton)
    } finally {
      setIsUploading(false);
    }
  };

<<<<<<< HEAD
  const getUploadedImages = async () => {
    try {
      setUploadedImagesLoading(true);
      const result = await ImagesApi.getUploadedImages();
      setUploadedImages(result);
    } catch (err:any) {
      toast.error(err.message || "Failed to get uploaded images. Please try again.");
      console.log("Get uploaded images error:", err.message);
    } finally {
      setUploadedImagesLoading(false);
    }
  };
  const handleTabChange = (value: string) => {
    if (value === "upload") {
      getUploadedImages();
    }
  };

  const handleDeleteImage = async (image_id: string) => {
    try {
      const result = await ImagesApi.deleteImage(image_id);
      setUploadedImages(uploadedImages.filter((image) => image.id !== image_id));
      toast.success(result.message || "Image deleted successfully");
    } catch (err:any) {
      toast.error(err.message || "Failed to delete image. Please try again.");
    }
  };
  return (
    <div className="image-editor-container">
      <Sheet open={isOpen} onOpenChange={() => handleClose()}>
=======
  // Helper function to determine image URL
  const getImageUrl = (src: string | null) => {
    if (!src) return "";
    return src.startsWith("user") ? `file://${src}` : `file://${src}`;
  };

  return (
    <>
      <div
        ref={imageContainerRef}
        className={cn(
          "relative group max-md:h-[200px] max-lg:h-[300px] max-md:pointer-events-none  lg:aspect-[4/4] w-full cursor-pointer rounded-lg overflow-hidden",
          isFocusPointMode ? "cursor-crosshair" : "",
          className
        )}
        data-slide-element
        data-slide-index={slideIndex}
        data-element-type="picture"
        data-element-id={elementId}
        onClick={(e) => {
          if (initialImage !== undefined) {
            if (isFocusPointMode) {
              handleFocusPointClick(e);
            } else {
              handleImageClick();
            }
          }
        }}
      >
        {image ? (
          <img
            ref={imageRef}
            src={getImageUrl(image)}
            alt={title}
            className="w-full h-full transition-all duration-200 "
            style={{
              objectFit: objectFit,
              objectPosition: `${focusPoint.x}% ${focusPoint.y}%`,
            }}
            data-slide-index={slideIndex}
            data-element-type="picture"
            data-is-image
            data-object-fit={objectFit}
            data-focial-point-x={focusPoint.x}
            data-focial-point-y={focusPoint.y}
            data-element-id={`${elementId}-image`}
            data-is-network={image && image.startsWith("http")}
            data-image-path={image}
          />
        ) : (
          <div className="w-full h-full relative">
            <Skeleton className="w-full h-full bg-gray-300 animate-pulse" />
            {
              <p className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full text-center text-sm text-gray-500">
                {initialImage !== undefined
                  ? "Click to add image"
                  : "Loading..."}
              </p>
            }
          </div>
        )}

        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-all duration-200 rounded-lg" />

        {isFocusPointMode && (
          <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
            <div className="text-white text-center p-2 bg-black/50 rounded">
              <p className="text-sm font-medium">
                Click anywhere to set focus point
              </p>
              <button
                className="mt-2 px-3 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600"
                onClick={(e) => {
                  e.stopPropagation();
                  toggleFocusPointMode();
                }}
              >
                Done
              </button>
            </div>

            {/* Focus point marker */}
            <div
              className="absolute w-8 h-8 border-2 border-white rounded-full transform -translate-x-1/2 -translate-y-1/2 pointer-events-none"
              style={{
                left: `${focusPoint.x}%`,
                top: `${focusPoint.y}%`,
                boxShadow: "0 0 0 2px rgba(0,0,0,0.5)",
              }}
            >
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-2 h-2 bg-white rounded-full"></div>
              </div>
              <div className="absolute w-16 h-0.5 bg-white/70 left-1/2 -translate-x-1/2"></div>
              <div className="absolute w-0.5 h-16 bg-white/70 top-1/2 -translate-y-1/2"></div>
            </div>
          </div>
        )}

        {/* Image Toolbar */}
        {isToolbarOpen && !isFocusPointMode && (
          <div
            ref={toolbarRef}
            className="absolute bottom-2 left-1/2 transform -translate-x-1/2 bg-white rounded-full shadow-lg z-10 toolbar-popover"
          >
            <div className="flex items-center p-1 space-x-1">
              <ToolTip content="Edit">
                <button
                  className="p-2 hover:bg-gray-100 rounded-full transition-colors "
                  onClick={handleOpenEditor}
                  title="Edit Image"
                >
                  <Edit className="w-4 h-4 text-gray-700" />
                </button>
              </ToolTip>
              <ToolTip content="Focus Point">
                <button
                  className="p-2 hover:bg-gray-100 rounded-full transition-colors "
                  onClick={toggleFocusPointMode}
                  title="Set Focus Point"
                >
                  <Move className="w-4 h-4 text-gray-700" />
                </button>
              </ToolTip>

              <Popover>
                <PopoverTrigger asChild>
                  <button
                    className="p-2 hover:bg-gray-100 rounded-full transition-colors "
                    title="Fit Options"
                  >
                    <Maximize className="w-4 h-4 text-gray-700" />
                  </button>
                </PopoverTrigger>
                <PopoverContent className="w-36 p-2" ref={popoverContentRef}>
                  <div className="flex flex-col space-y-1">
                    <button
                      className={cn(
                        "text-left px-2 py-1 text-sm rounded flex items-center",
                        objectFit === "cover"
                          ? "bg-blue-100 text-blue-800"
                          : "hover:bg-gray-100"
                      )}
                      onClick={(e) => {
                        e.preventDefault();
                        handleFitChange("cover");
                      }}
                    >
                      <div className="w-4 h-4 mr-2 border border-current rounded overflow-hidden relative">
                        <div className="absolute inset-0 bg-current opacity-20"></div>
                        <div className="absolute inset-0 flex items-center justify-center">
                          <div className="w-2 h-3 bg-current rounded-sm"></div>
                        </div>
                      </div>
                      Cover
                    </button>
                    <button
                      className={cn(
                        "text-left px-2 py-1 text-sm rounded flex items-center",
                        objectFit === "contain"
                          ? "bg-blue-100 text-blue-800"
                          : "hover:bg-gray-100"
                      )}
                      onClick={(e) => {
                        e.preventDefault();
                        handleFitChange("contain");
                      }}
                    >
                      <div className="w-4 h-4 mr-2 border border-current rounded overflow-hidden relative">
                        <div className="absolute inset-0 bg-current opacity-20"></div>
                        <div className="absolute inset-0 flex items-center justify-center">
                          <div className="w-3 h-2 bg-current rounded-sm"></div>
                        </div>
                      </div>
                      Contain
                    </button>
                    <button
                      className={cn(
                        "text-left px-2 py-1 text-sm rounded flex items-center",
                        objectFit === "fill"
                          ? "bg-blue-100 text-blue-800"
                          : "hover:bg-gray-100"
                      )}
                      onClick={(e) => {
                        e.preventDefault();
                        handleFitChange("fill");
                      }}
                    >
                      <div className="w-4 h-4 mr-2 border border-current rounded overflow-hidden relative">
                        <div className="absolute inset-0 bg-current opacity-20"></div>
                        <div className="absolute inset-0 flex items-center justify-center">
                          <div className="w-3 h-3 bg-current rounded-sm"></div>
                        </div>
                      </div>
                      Fill
                    </button>
                  </div>
                </PopoverContent>
              </Popover>
            </div>
          </div>
        )}
      </div>

      <Sheet open={isEditorOpen} onOpenChange={setIsEditorOpen}>
>>>>>>> 78e1006 (Initial: presenton)
        <SheetContent
          side="right"
          className="w-[600px]"
          onOpenAutoFocus={(e) => e.preventDefault()}
<<<<<<< HEAD
          onClick={(e) => e.stopPropagation()}
=======
>>>>>>> 78e1006 (Initial: presenton)
        >
          <SheetHeader>
            <SheetTitle>Update Image</SheetTitle>
          </SheetHeader>

          <div className="mt-6">
<<<<<<< HEAD
            <Tabs defaultValue="generate" className="w-full" onValueChange={handleTabChange}>
              <TabsList className="grid bg-blue-100 border border-blue-300 w-full grid-cols-3 mx-auto">
                <TabsTrigger className="font-medium" value="generate">
                  AI Generate
                </TabsTrigger>
                <TabsTrigger className="font-medium" value="upload">
                  Upload
                </TabsTrigger>
                <TabsTrigger className="font-medium" value="edit">
                  Edit
                </TabsTrigger>
              </TabsList>
              {/* Generate Tab */}
              <TabsContent value="generate" className="mt-4 space-y-4 overflow-y-auto hide-scrollbar h-[85vh]">
                <div className="space-y-4">
                  <div>
                    <h3 className="text-sm font-medium mb-1">Current Prompt</h3>
                    <p className="text-sm text-gray-500">{promptContent}</p>
                  </div>

=======
            <Tabs defaultValue="generate" className="w-full">
              <TabsList className="grid bg-blue-100 border border-blue-300 w-full grid-cols-3">
                <TabsTrigger className="font-medium" value="generate">
                  AI Generate
                </TabsTrigger>
                <TabsTrigger
                  className="font-medium"
                  onClick={handleSearchImage}
                  value="search"
                >
                  Web Images
                </TabsTrigger>
                <TabsTrigger className="font-medium" value="upload">
                  Upload
                </TabsTrigger>
              </TabsList>

              <TabsContent value="generate" className="mt-4 space-y-4">
                <div></div>
                <div className="space-y-4">
                  <div className="">
                    <h3 className="text-sm font-medium mb-1">Current Prompt</h3>

                    <p className="text-sm text-gray-500">{promptContent}</p>
                  </div>
>>>>>>> 78e1006 (Initial: presenton)
                  <div>
                    <h3 className="text-base font-medium mb-2">
                      Image Description
                    </h3>
                    <Textarea
                      placeholder="Describe the image you want to generate..."
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      className="min-h-[100px]"
                    />
                  </div>
<<<<<<< HEAD

=======
>>>>>>> 78e1006 (Initial: presenton)
                  <Button
                    onClick={handleGenerateImage}
                    className="w-full"
                    disabled={!prompt || isGenerating}
                  >
                    <Wand2 className="w-4 h-4 mr-2" />
                    {isGenerating ? "Generating..." : "Generate Image"}
                  </Button>

                  {error && <p className="text-red-500 text-sm">{error}</p>}

                  <div className="grid grid-cols-2 gap-4">
<<<<<<< HEAD
                    {isGenerating || !previewImages ? (
                      Array.from({ length: 4 }).map((_, index) => (
=======
                    {isGenerating || previewImages.length === 0
                      ? Array.from({ length: 4 }).map((_, index) => (
                          <Skeleton
                            key={index}
                            className="aspect-[4/3] w-full rounded-lg"
                          />
                        ))
                      : previewImages.map((image, index) => (
                          <div
                            key={index}
                            onClick={() => handleImageChange(image as string)}
                            className="aspect-[4/3] w-full overflow-hidden rounded-lg border cursor-pointer"
                          >
                            <img
                              src={
                                image
                                  ? image.startsWith("user")
                                    ? `${PresentationGenerationApi.BASE_URL}${image}`
                                    : image
                                  : ""
                              }
                              alt={`Preview ${index + 1}`}
                              className="w-full h-full object-cover"
                            />
                          </div>
                        ))}
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="search" className="mt-4 space-y-4">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSearchImage();
                  }}
                >
                  <div className="relative mb-3">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 w-4 h-4" />
                    <Input
                      placeholder="Search images..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                  <Button
                    type="submit"
                    variant="outline"
                    className="w-full text-semibold text-[#51459e]"
                  >
                    Search
                  </Button>
                </form>
                {error && <p className="text-red-500 text-sm">{error}</p>}

                <div className="grid grid-cols-2 gap-4 max-h-[80vh] hide-scrollbar overflow-y-auto">
                  {isSearching
                    ? Array.from({ length: 6 }).map((_, index) => (
>>>>>>> 78e1006 (Initial: presenton)
                        <Skeleton
                          key={index}
                          className="aspect-[4/3] w-full rounded-lg"
                        />
                      ))
<<<<<<< HEAD
                    ) : (
                      <div
                        onClick={() => handleImageChange(previewImages)}
                        className="aspect-[4/3] w-full overflow-hidden rounded-lg border cursor-pointer hover:border-blue-500 transition-colors"
                      >
                        {previewImages && (
                          <img
                            src={previewImages}
                            alt={`Preview`}
                            className="w-full h-full object-cover"
                          />
                        )}
                      </div>
                    )}
                  </div>
                  {previousGeneratedImages.length > 0 && (
                    <div className="mt-4">
                      <h3 className="text-sm font-medium mb-2">
                        Previous Generated Images
                      </h3>
                      <div className="grid grid-cols-2 gap-4  ">
                        {previousGeneratedImages.map((image) => (
                          <div
                            onClick={() => handleImageChange(image.path)}
                            key={image.id}
                            className="aspect-[4/3] w-full overflow-hidden rounded-lg border cursor-pointer hover:border-blue-500 transition-colors"
                          >
                            <img
                              src={image.path}
                              alt={image.extras.prompt}
                              className="w-full h-full object-cover"
                            />
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </TabsContent>

              {/* Upload Tab */}
=======
                    : searchedImages.map((imgSrc, index) => (
                        <div
                          key={index}
                          onClick={() => handleImageChange(imgSrc)}
                          className="aspect-[4/3] cursor-pointer group relative rounded-lg overflow-hidden"
                        >
                          <img
                            src={imgSrc}
                            alt={`Search result ${index + 1}`}
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                          />
                          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-200" />
                        </div>
                      ))}
                </div>
              </TabsContent>

>>>>>>> 78e1006 (Initial: presenton)
              <TabsContent value="upload" className="mt-4 space-y-4">
                <div className="space-y-4">
                  <div
                    className={cn(
                      "border-2 border-dashed rounded-lg p-8 text-center transition-colors",
                      isUploading
                        ? "border-gray-400 bg-gray-50"
<<<<<<< HEAD
                        : "border-gray-300 hover:border-blue-400"
=======
                        : "border-gray-300"
>>>>>>> 78e1006 (Initial: presenton)
                    )}
                  >
                    <input
                      type="file"
                      id="file-upload"
                      className="hidden"
                      accept="image/*"
                      onChange={handleFileUpload}
                      disabled={isUploading}
                    />
                    <label
                      htmlFor="file-upload"
                      className={cn(
                        "flex flex-col items-center",
                        isUploading ? "cursor-wait" : "cursor-pointer"
                      )}
                    >
                      {isUploading ? (
                        <div className="w-8 h-8 border-2 border-gray-400 border-t-transparent rounded-full animate-spin mb-2" />
                      ) : (
                        <Upload className="w-8 h-8 text-gray-500 mb-2" />
                      )}
                      <span className="text-sm text-gray-600">
                        {isUploading
                          ? "Uploading your image..."
                          : "Click to upload an image"}
                      </span>
                      <span className="text-xs text-gray-500 mt-1">
                        Maximum file size: 5MB
                      </span>
                    </label>
                  </div>
<<<<<<< HEAD

=======
>>>>>>> 78e1006 (Initial: presenton)
                  {uploadError && (
                    <p className="text-red-500 text-sm text-center">
                      {uploadError}
                    </p>
                  )}

                  {(uploadedImageUrl || isUploading) && (
                    <div className="mt-4">
                      <h3 className="text-sm font-medium mb-2">
                        Uploaded Image Preview
                      </h3>
                      <div className="aspect-[4/3] relative rounded-lg overflow-hidden border border-gray-200">
                        {isUploading ? (
                          <div className="w-full h-full bg-gray-100 flex items-center justify-center">
                            <div className="flex flex-col items-center">
                              <div className="w-8 h-8 border-2 border-gray-400 border-t-transparent rounded-full animate-spin mb-2" />
                              <span className="text-sm text-gray-500">
                                Processing...
                              </span>
                            </div>
                          </div>
                        ) : (
                          uploadedImageUrl && (
                            <div
                              onClick={() =>
                                handleImageChange(uploadedImageUrl)
                              }
                              className="cursor-pointer group w-full h-full"
                            >
                              <img
                                src={uploadedImageUrl}
                                alt="Uploaded preview"
                                className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                              />
                              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-200" />
                              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                                <span className="bg-white/90 px-3 py-1 rounded-full text-sm font-medium">
                                  Click to use this image
                                </span>
                              </div>
                            </div>
                          )
                        )}
                      </div>
                    </div>
                  )}
<<<<<<< HEAD
                  <div>
                    <h3 className="text-sm font-medium mb-2">Uploaded Images:</h3>
                    <div className="grid grid-cols-2 gap-4">
                      {uploadedImagesLoading ? (
                        <div className="flex items-center justify-center">
                          <Loader2 className="w-4 h-4 animate-spin" />
                        </div>
                      ) : (
                        uploadedImages.map((image) => (
                          <div key={image.id}>
                            <div
                              onClick={() =>
                                handleImageChange(image.path)
                              }
                              className="cursor-pointer group aspect-[4/3] rounded-lg overflow-hidden relative border border-gray-200"
                            >
                              <Trash className="absolute group-hover:opacity-100 opacity-0 transition-opacity z-10 w-4 h-4 top-2 right-2 text-red-500" onClick={(e) =>{
                                e.stopPropagation();
                                handleDeleteImage(image.id)
                              }}/>
                              <img
                                src={image.path}
                                alt="Uploaded preview"
                                className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                              />
                              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-200" />
                              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                                <span className="bg-white/90 px-3 py-1 rounded-full text-xs font-medium">
                                  Use
                                </span>
                              </div>
                            </div>
                          
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                </div>
              </TabsContent>
              <TabsContent value="edit" className="mt-4 space-y-4">
                <div className="space-y-4">
                  <h3 className="text-sm font-medium mb-2">Current Image</h3>
                  <div
                    onClick={(e) => {
                      if (isFocusPointMode) {
                        handleFocusPointClick(e);
                      } else {
                      }
                    }}
                    className="aspect-[4/3] group  rounded-lg overflow-hidden relative border border-gray-200"
                  >
                    <p className="group-hover:opacity-100 opacity-0 transition-opacity absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-sm text-center font-medium bg-black/50 text-white px-2 py-1 rounded">
                      Click to Change Focus Point
                    </p>
                    {previewImages && (
                      <img
                        ref={imageRef}
                        onClick={() => {
                          setIsFocusPointMode(true);
                        }}
                        src={previewImages}
                        style={{
                          objectFit: objectFit,
                          objectPosition: `${focusPoint.x}% ${focusPoint.y}%`,
                        }}
                        alt={`Preview`}
                        className="w-full h-full "
                      />
                    )}
                    {isFocusPointMode && (
                      <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
                        <div className="text-white text-center p-2 bg-black/50 rounded">
                          <p className="text-sm font-medium pointer-events-none">
                            Click anywhere to set focus point
                          </p>
                          <button
                            className="mt-2 px-3 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600"
                            onClick={(e) => {
                              e.stopPropagation();
                              toggleFocusPointMode();
                            }}
                          >
                            Done
                          </button>
                        </div>

                        <div
                          className="absolute w-8 h-8 border-2 border-white rounded-full transform -translate-x-1/2 -translate-y-1/2 pointer-events-none"
                          style={{
                            left: `${focusPoint.x}%`,
                            top: `${focusPoint.y}%`,
                            boxShadow: "0 0 0 2px rgba(0,0,0,0.5)",
                          }}
                        >
                          <div className="absolute inset-0 flex items-center justify-center">
                            <div className="w-2 h-2 bg-white rounded-full"></div>
                          </div>
                          <div className="absolute w-16 h-0.5 bg-white/70 left-1/2 -translate-x-1/2"></div>
                          <div className="absolute w-0.5 h-16 bg-white/70 top-1/2 -translate-y-1/2"></div>
                        </div>
                      </div>
                    )}
                  </div>
                  {/* Edit Image  */}
                  {/* Object Fit */}
                  {
                    <div>
                      <h3 className="text-sm font-medium mb-2">Object Fit</h3>
                      <div className="flex gap-4">
                        <Button
                          variant="outline"
                          className={cn(
                            objectFit === "cover" &&
                              "bg-blue-50 border-blue-500"
                          )}
                          onClick={() => handleFitChange("cover")}
                        >
                          Cover
                        </Button>
                        <Button
                          variant="outline"
                          className={cn(
                            objectFit === "contain" &&
                              "bg-blue-50 border-blue-500"
                          )}
                          onClick={() => handleFitChange("contain")}
                        >
                          Contain
                        </Button>
                        <Button
                          variant="outline"
                          className={cn(
                            objectFit === "fill" && "bg-blue-50 border-blue-500"
                          )}
                          onClick={() => handleFitChange("fill")}
                        >
                          Fill
                        </Button>
                      </div>
                    </div>
                  }
                  {/* Focus Point */}
                  {}
=======
>>>>>>> 78e1006 (Initial: presenton)
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </SheetContent>
      </Sheet>
<<<<<<< HEAD
    </div>
=======
    </>
>>>>>>> 78e1006 (Initial: presenton)
  );
};

export default React.memo(ImageEditor);
