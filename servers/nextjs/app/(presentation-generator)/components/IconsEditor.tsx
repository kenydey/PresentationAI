"use client";
import React, { useEffect, useState } from "react";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Input } from "@/components/ui/input";
<<<<<<< HEAD
import { Search } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { PresentationGenerationApi } from "../services/api/presentation-generation";
import { getStaticFileUrl } from "../utils/others";
import { toast } from "sonner";
interface IconsEditorProps {
  icon_prompt?: string[] | null;
  onClose?: () => void;
  onIconChange?: (newIconUrl: string, query?: string) => void;
}

const IconsEditor = ({
  icon_prompt,
  onClose,
  onIconChange,

}: IconsEditorProps) => {
  // State management
  const [icons, setIcons] = useState<string[]>([]);
=======
import { PlusIcon, Search } from "lucide-react";
import { cn } from "@/lib/utils";
import { useDispatch, useSelector } from "react-redux";
import { PresentationGenerationApi } from "../services/api/presentation-generation";
import { RootState } from "@/store/store";
import { usePathname } from "next/navigation";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { updateSlideIcon } from "@/store/slices/presentationGeneration";

interface IconsEditorProps {
  icon: string;
  index: number;
  backgroundColor: string;
  hasBg: boolean;
  slideIndex: number;
  elementId: string;
  isWhite?: boolean;
  className?: string;
  icon_prompt?: string[] | null;
}

const IconsEditor = ({
  icon: initialIcon,
  index,
  backgroundColor,
  hasBg,
  className,
  slideIndex,
  elementId,
  icon_prompt,
}: IconsEditorProps) => {
  const dispatch = useDispatch();

  const [icon, setIcon] = useState(initialIcon);
  const [icons, setIcons] = useState<string[]>([]);
  const [isEditorOpen, setIsEditorOpen] = useState(false);
>>>>>>> 78e1006 (Initial: presenton)
  const [searchQuery, setSearchQuery] = useState<string>(
    icon_prompt?.[0] || ""
  );
  const [loading, setLoading] = useState(true);
<<<<<<< HEAD
  const [isOpen, setIsOpen] = useState(true);

  // Search for icons when component opens
  useEffect(() => {
    if (icon_prompt && icon_prompt.length > 0 && icons.length === 0) {
      handleIconSearch();
    }
  }, []);

  /**
   * Searches for icons based on the current query
   */
  const handleIconSearch = async () => {
    setLoading(true);
=======
  const path = usePathname();

  useEffect(() => {
    setIcon(initialIcon);
  }, [initialIcon]);

  useEffect(() => {
    if (isEditorOpen) {
      handleIconSearch();
    }
  }, [isEditorOpen]);

  const handleIconClick = () => {
    setIsEditorOpen(true);
  };

  const handleIconSearch = async () => {
    setLoading(true);
    const presentation_id = path.split("/")[2];
>>>>>>> 78e1006 (Initial: presenton)
    const query = searchQuery.length > 0 ? searchQuery : icon_prompt?.[0] || "";

    try {
      const data = await PresentationGenerationApi.searchIcons({
<<<<<<< HEAD
        query,
        limit: 40,
      });
      setIcons(data);
    } catch (error: any) {
      console.error("Error fetching icons:", error);
      toast.error(error.message || "Failed to fetch icons. Please try again.");
=======
        presentation_id,
        query,
        page: 1,
        limit: 40,
      });
      setIcons(data.urls);
    } catch (error) {
      console.error("Error fetching icons:", error);
>>>>>>> 78e1006 (Initial: presenton)
      setIcons([]);
    } finally {
      setLoading(false);
    }
  };

<<<<<<< HEAD
  /**
   * Handles icon selection and calls the parent callback
   */
  const handleIconChange = (newIcon: string) => {

    if (onIconChange) {
      onIconChange(newIcon, searchQuery || icon_prompt?.[0] || '');
    }
    handleClose();
  };

  // Handle close with animation
  const handleClose = () => {
    setIsOpen(false);
    // Delay the actual close to allow animation to complete
    setTimeout(() => {
      onClose?.();
    }, 300); // Match the Sheet animation duration
  };
  

  return (
    <div className="icons-editor-container">


      <Sheet open={isOpen} onOpenChange={() => handleClose()}>
=======
  const handleIconChange = (newIcon: string) => {


    setIcon(newIcon);
    dispatch(
      updateSlideIcon({ index: slideIndex, iconIdx: index, icon: newIcon })
    );
    setIsEditorOpen(false);
  };

  return (
    <>
      <div
        style={{ background: hasBg ? backgroundColor : "transparent" }}
        onClick={handleIconClick}
        className={cn(
          "relative overflow-hidden w-[34px] h-[34px] md:w-[64px] max-md:pointer-events-none md:h-[64px] flex items-center justify-center cursor-pointer group",
          hasBg && ` rounded-[50%]`,
          className
        )}
        data-slide-element
        data-slide-index={slideIndex}
        data-element-type={hasBg ? "filledbox" : "emptybox"}
        data-element-id={`${elementId}-container`}
      >
        {icon ? (
          <img
            src={`file://${icon}`}
            alt="slide icon"
            className={`object-contain w-[16px] h-[16px] md:w-[32px] md:h-[32px] ${hasBg ? "brightness-0 invert" : ""
              }`}
            data-slide-element
            style={{
              filter: hasBg
                ? "brightness(0) invert"
                : "sepia(100%) hue-rotate(190deg) saturate(500%)",
            }}
            data-slide-index={slideIndex}
            data-element-type="picture"
            data-is-icon
            data-element-id={`${elementId}-image`}
            data-is-network={false}
            data-image-path={icon}
          />
        ) : (
          <div className="w-[32px] h-[32px] relative">
            <Skeleton className="w-[32px] h-[32px] bg-gray-100 " />
            {initialIcon !== undefined && (
              <p className="absolute top-1/2 left-1/2  -translate-x-[30%] -translate-y-1/2 w-full text-center text-sm text-[#51459e]">
                <PlusIcon className="w-5 h-5" />
              </p>
            )}
          </div>
        )}
        {/* Hover overlay */}
        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-all duration-200" />
      </div>

      <Sheet open={isEditorOpen} onOpenChange={setIsEditorOpen}>
>>>>>>> 78e1006 (Initial: presenton)
        <SheetContent
          side="right"
          className="w-[400px]"
          onOpenAutoFocus={(e) => e.preventDefault()}
<<<<<<< HEAD
          onClick={(e) => e.stopPropagation()}
=======
>>>>>>> 78e1006 (Initial: presenton)
        >
          <SheetHeader>
            <SheetTitle>Choose Icon</SheetTitle>
          </SheetHeader>
<<<<<<< HEAD

          <div className="mt-6 space-y-4">
            {/* Search Form */}
            <form
              onSubmit={(e) => {
                e.preventDefault();
                e.stopPropagation();
=======
          <div className="mt-6 space-y-4">
            <form
              onSubmit={(e) => {
                e.preventDefault();
>>>>>>> 78e1006 (Initial: presenton)
                handleIconSearch();
              }}
            >
              <div className="relative mb-3">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 w-4 h-4" />
<<<<<<< HEAD
=======

>>>>>>> 78e1006 (Initial: presenton)
                <Input
                  placeholder="Search icons..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
<<<<<<< HEAD
                  onClick={(e) => e.stopPropagation()}
=======
>>>>>>> 78e1006 (Initial: presenton)
                  className="pl-10"
                />
              </div>
              <Button
                type="submit"
                variant="outline"
                className="w-full text-semibold text-[#51459e]"
<<<<<<< HEAD
                onClick={(e) => e.stopPropagation()}
=======
>>>>>>> 78e1006 (Initial: presenton)
              >
                Search
              </Button>
            </form>

<<<<<<< HEAD
            {/* Icons Grid */}
=======
            {/* Icons grid */}
>>>>>>> 78e1006 (Initial: presenton)
            <div className="max-h-[80vh] hide-scrollbar overflow-y-auto p-1">
              {loading ? (
                <div className="grid grid-cols-4 gap-4">
                  {Array.from({ length: 40 }).map((_, index) => (
                    <Skeleton key={index} className="w-16 h-16 rounded-lg" />
                  ))}
                </div>
<<<<<<< HEAD
              ) : icons && icons.length > 0 ? (
=======
              ) : icons.length > 0 ? (
>>>>>>> 78e1006 (Initial: presenton)
                <div className="grid grid-cols-4 gap-4">
                  {icons.map((iconSrc, idx) => (
                    <div
                      key={idx}
<<<<<<< HEAD
                      onClick={(e) => {
                        e.stopPropagation();
                        handleIconChange(iconSrc);
                      }}
                      className="w-12 h-12 cursor-pointer group relative rounded-lg overflow-hidden hover:bg-gray-100 p-2 transition-colors"
=======
                      onClick={() => handleIconChange(iconSrc)}
                      className="w-12 h-12 cursor-pointer group relative rounded-lg overflow-hidden hover:bg-gray-100 p-2"
>>>>>>> 78e1006 (Initial: presenton)
                    >
                      <img
                        src={iconSrc}
                        alt={`Icon ${idx + 1}`}
<<<<<<< HEAD
                        className="w-full h-full object-contain"
=======
                        className="w-full h-full object-contain "
>>>>>>> 78e1006 (Initial: presenton)
                      />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center w-full h-[60vh] text-center text-gray-500 space-y-4">
                  <Search className="w-12 h-12 text-gray-400" />
                  <p className="text-sm">No icons found for your search.</p>
                  <p className="text-xs">Try refining your search query.</p>
                </div>
              )}
            </div>
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

export default IconsEditor;
