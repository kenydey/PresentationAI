"use client";
import { Button } from "@/components/ui/button";
import {
<<<<<<< HEAD
  SquareArrowOutUpRight,
  Play,
  Loader2,
  Redo2,
  Undo2,

} from "lucide-react";
import React, { useState } from "react";
import Wrapper from "@/components/Wrapper";
import { useRouter, usePathname } from "next/navigation";
=======
  Menu,
  Palette,
  SquareArrowOutUpRight,
  Play,
  Loader2,
  Copy,
  Zap,
} from "lucide-react";
import React, { useEffect, useState } from "react";
import Image from "next/image";
import Wrapper from "@/components/Wrapper";
import { usePathname, useRouter } from "next/navigation";
>>>>>>> 78e1006 (Initial: presenton)
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
<<<<<<< HEAD
import { PresentationGenerationApi } from "../../services/api/presentation-generation";
import { OverlayLoader } from "@/components/ui/overlay-loader";
=======
import UserAccount from "../../components/UserAccount";
import { PresentationGenerationApi } from "../../services/api/presentation-generation";
import { OverlayLoader } from "@/components/ui/overlay-loader";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
>>>>>>> 78e1006 (Initial: presenton)
import { useDispatch, useSelector } from "react-redux";

import Link from "next/link";

<<<<<<< HEAD
import { RootState } from "@/store/store";
import { toast } from "sonner";


import Announcement from "@/components/Announcement";
import { PptxPresentationModel } from "@/types/pptx_models";
import HeaderNav from "../../components/HeaderNab";
import PDFIMAGE from "@/public/pdf.svg";
import PPTXIMAGE from "@/public/pptx.svg";
import Image from "next/image";
import { trackEvent, MixpanelEvent } from "@/utils/mixpanel";
import { usePresentationUndoRedo } from "../hooks/PresentationUndoRedo";
import ToolTip from "@/components/ToolTip";
import { clearPresentationData } from "@/store/slices/presentationGeneration";
import { clearHistory } from "@/store/slices/undoRedoSlice";
=======
import { ThemeType } from "@/app/(presentation-generator)/upload/type";
import {
  setTheme,
  setThemeColors,
  defaultColors,
  serverColors,
} from "../../store/themeSlice";
import CustomThemeSettings from "../../components/CustomThemeSettings";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { RootState } from "@/store/store";
import { toast } from "@/hooks/use-toast";

import ThemeSelector from "./ThemeSelector";
import Modal from "./Modal";

import Announcement from "@/components/Announcement";
>>>>>>> 78e1006 (Initial: presenton)

const Header = ({
  presentation_id,
  currentSlide,
}: {
  presentation_id: string;
  currentSlide?: number;
}) => {
  const [open, setOpen] = useState(false);
  const [showLoader, setShowLoader] = useState(false);
  const router = useRouter();
  const pathname = usePathname();
<<<<<<< HEAD
  const dispatch = useDispatch();


  const { presentationData, isStreaming } = useSelector(
    (state: RootState) => state.presentationGeneration
  );

  const { onUndo, onRedo, canUndo, canRedo } = usePresentationUndoRedo();

  const get_presentation_pptx_model = async (id: string): Promise<PptxPresentationModel> => {
    const response = await fetch(`/api/presentation_to_pptx_model?id=${id}`);
    const pptx_model = await response.json();
    return pptx_model;
  };

=======

  const [showCustomThemeModal, setShowCustomThemeModal] = useState(false);
  const { currentTheme, currentColors } = useSelector(
    (state: RootState) => state.theme
  );
  const { presentationData, isStreaming } = useSelector(
    (state: RootState) => state.presentationGeneration
  );
  const dispatch = useDispatch();
  const handleThemeSelect = async (value: string) => {
    if (isStreaming) return;
    if (value === "custom") {
      setShowCustomThemeModal(true);
      return;
    } else {
      const themeType = value as ThemeType;
      const themeColors = serverColors[themeType] || defaultColors[themeType];

      if (themeColors) {
        try {
          // Update UI
          dispatch(setTheme(themeType));
          dispatch(setThemeColors({ ...themeColors, theme: themeType }));
          // Set CSS variables
          const root = document.documentElement;
          root.style.setProperty(
            `--${themeType}-slide-bg`,
            themeColors.slideBg
          );
          root.style.setProperty(
            `--${themeType}-slide-title`,
            themeColors.slideTitle
          );
          root.style.setProperty(
            `--${themeType}-slide-heading`,
            themeColors.slideHeading
          );
          root.style.setProperty(
            `--${themeType}-slide-description`,
            themeColors.slideDescription
          );
          root.style.setProperty(
            `--${themeType}-slide-box`,
            themeColors.slideBox
          );

          // Save in background
          await PresentationGenerationApi.setThemeColors(presentation_id, {
            name: themeType,
            colors: {
              ...themeColors,
            },
          });
        } catch (error) {
          console.error("Failed to update theme:", error);
          toast({
            title: "Error updating theme",
            description:
              "Failed to update the presentation theme. Please try again.",
            variant: "destructive",
          });
        }
      }
    }
  };

  const getSlideMetadata = async () => {
    try {
      const response = await fetch(
        "http://localhost:3000/api/slide-metadata",
        {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            url: window.location.href,
            theme: currentTheme,
            customColors: currentColors,
          }),
        }
      );


      if (!response.ok) {
        throw new Error("Failed to fetch metadata");
      }
      const metadata = await response.json();
      console.log("metadata", metadata);
      return metadata;
    } catch (error) {
      setShowLoader(false);
      console.error("Error fetching metadata:", error);
      // You might want to show an error toast/notification here
      throw error;
    }
  };
  const metaData = async () => {
    const body = {
      presentation_id: presentation_id,
      slides: presentationData?.slides,
    };
    await PresentationGenerationApi.updatePresentationContent(body)
      .then(() => { })
      .catch((error) => {
        console.error(error);
      });

    const metadata = await getSlideMetadata();

    const slides = metadata.map((slide: any, index: any) => {
      return {
        shapes: slide.elements,
      };
    });

    const apiBody = {
      presentation_id: presentation_id,
      pptx_model: {
        background_color: metadata[0].backgroundColor,

        slides: slides,
      },
    };

    return apiBody;
  };
>>>>>>> 78e1006 (Initial: presenton)
  const handleExportPptx = async () => {
    if (isStreaming) return;

    try {
      setOpen(false);
      setShowLoader(true);
<<<<<<< HEAD
      // Save the presentation data before exporting
      trackEvent(MixpanelEvent.Header_UpdatePresentationContent_API_Call);
      await PresentationGenerationApi.updatePresentationContent(presentationData);
      trackEvent(MixpanelEvent.Header_GetPptxModel_API_Call);
      const pptx_model = await get_presentation_pptx_model(presentation_id);
      if (!pptx_model) {
        throw new Error("Failed to get presentation PPTX model");
      }
      trackEvent(MixpanelEvent.Header_ExportAsPPTX_API_Call);
      const pptx_path = await PresentationGenerationApi.exportAsPPTX(pptx_model);
      if (pptx_path) {
        // window.open(pptx_path, '_self');
        downloadLink(pptx_path);
      } else {
        throw new Error("No path returned from export");
=======

      const apiBody = await metaData();

      const response = await PresentationGenerationApi.exportAsPPTX(apiBody);
      if (response.url) {
        downloadLink(response.url);
      } else {
        throw new Error("No URL returned from export");
>>>>>>> 78e1006 (Initial: presenton)
      }
    } catch (error) {
      console.error("Export failed:", error);
      setShowLoader(false);
<<<<<<< HEAD
      toast.error("Having trouble exporting!", {
        description:
          "We are having trouble exporting your presentation. Please try again.",
=======
      toast({
        title: "Having trouble exporting!",
        description:
          "We are having trouble exporting your presentation. Please try again.",
        variant: "default",
>>>>>>> 78e1006 (Initial: presenton)
      });
    } finally {
      setShowLoader(false);
    }
  };
<<<<<<< HEAD

=======
  const downloadLink = (url: string) => {
    const link = document.createElement("a");
    link.href = url;
    // Append to document, trigger click and remove
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
>>>>>>> 78e1006 (Initial: presenton)
  const handleExportPdf = async () => {
    if (isStreaming) return;

    try {
      setOpen(false);
      setShowLoader(true);
<<<<<<< HEAD
      // Save the presentation data before exporting
      trackEvent(MixpanelEvent.Header_UpdatePresentationContent_API_Call);
      await PresentationGenerationApi.updatePresentationContent(presentationData);

      trackEvent(MixpanelEvent.Header_ExportAsPDF_API_Call);
      const response = await fetch('/api/export-as-pdf', {
        method: 'POST',
        body: JSON.stringify({
          id: presentation_id,
          title: presentationData?.title,
        })
      });

      if (response.ok) {
        const { path: pdfPath } = await response.json();
        // window.open(pdfPath, '_blank');
        downloadLink(pdfPath);
      } else {
        throw new Error("Failed to export PDF");
      }

    } catch (err) {
      console.error(err);
      toast.error("Having trouble exporting!", {
        description:
          "We are having trouble exporting your presentation. Please try again.",
      });
    } finally {
      setShowLoader(false);
    }
  };
  const handleReGenerate = () => {
    dispatch(clearPresentationData());
    dispatch(clearHistory())
    trackEvent(MixpanelEvent.Header_ReGenerate_Button_Clicked, { pathname });
    router.push(`/presentation?id=${presentation_id}&stream=true`);
  };
  const downloadLink = (path: string) => {
    // if we have popup access give direct download if not redirect to the path
    if (window.opener) {
      window.open(path, '_blank');
    } else {
      const link = document.createElement('a');
      link.href = path;
      link.download = path.split('/').pop() || 'download';
      document.body.appendChild(link);
      link.click();
    }
  };

  const ExportOptions = ({ mobile }: { mobile: boolean }) => (
    <div className={`space-y-2 max-md:mt-4 ${mobile ? "" : "bg-white"} rounded-lg`}>
      <Button
        onClick={() => {
          trackEvent(MixpanelEvent.Header_Export_PDF_Button_Clicked, { pathname });
          handleExportPdf();
        }}
        variant="ghost"
        className={`pb-4 border-b rounded-none border-gray-300 w-full flex justify-start text-[#5146E5] ${mobile ? "bg-white py-6 border-none rounded-lg" : ""}`} >
        <Image src={PDFIMAGE} alt="pdf export" width={30} height={30} />
        Export as PDF
      </Button>
      <Button
        onClick={() => {
          trackEvent(MixpanelEvent.Header_Export_PPTX_Button_Clicked, { pathname });
          handleExportPptx();
        }}
        variant="ghost"
        className={`w-full flex justify-start text-[#5146E5] ${mobile ? "bg-white py-6" : ""}`}
      >
        <Image src={PPTXIMAGE} alt="pptx export" width={30} height={30} />
        Export as PPTX
      </Button>


    </div>
  );

  const MenuItems = ({ mobile }: { mobile: boolean }) => (
    <div className="flex flex-col lg:flex-row items-center gap-4">
      {/* undo redo */}
      <button onClick={handleReGenerate} disabled={isStreaming || !presentationData} className="text-white  disabled:opacity-50" >

        Re-Generate
      </button>
      <div className="flex items-center gap-2 ">
        <ToolTip content="Undo">
          <button disabled={!canUndo} className="text-white disabled:opacity-50" onClick={() => {
            onUndo();
          }}>

            <Undo2 className="w-6 h-6 " />

          </button>
        </ToolTip>
        <ToolTip content="Redo">

          <button disabled={!canRedo} className="text-white disabled:opacity-50" onClick={() => {
            onRedo();
          }}>
            <Redo2 className="w-6 h-6 " />

          </button>
        </ToolTip>

      </div>

      {/* Present Button */}
      <Button
        onClick={() => {
          const to = `?id=${presentation_id}&mode=present&slide=${currentSlide || 0}`;
          trackEvent(MixpanelEvent.Navigation, { from: pathname, to });
          router.push(to);
        }}
=======
      const apiBody = await metaData();

      const data = await PresentationGenerationApi.exportAsPDF(apiBody);

      if (data.url) {
        downloadLink(data.url);
      }
      setShowLoader(false);
    } catch (err) {
      console.error(err);
      setShowLoader(false);
      toast({
        title: "Having trouble exporting!",
        description:
          "We are having trouble exporting your presentation. Please try again.",
        variant: "default",
      });
    }
  };

  const ExportOptions = () => (
    <div className="space-y-2 max-md:mt-4 bg-white rounded-lg p-2">
      <Button
        onClick={handleExportPdf}
        variant="ghost"
        className="pb-4 border-b rounded-none border-gray-300 w-full flex justify-start text-[#5146E5]"
      >
        <Image src="/pdf.svg" alt="pdf export" width={30} height={30} />
        Export as PDF
      </Button>
      <Button
        onClick={handleExportPptx}
        variant="ghost"
        className="w-full flex justify-start text-[#5146E5]"
      >
        <Image src="/pptx.svg" alt="pptx export" width={30} height={30} />
        Export as PPTX
      </Button>
    </div>
  );

  const MenuItems = () => (
    <div className="flex flex-col lg:flex-row items-center gap-4">
      {/* Present Button */}
      <Button
        onClick={() => router.push(`?mode=present&slide=${currentSlide || 0}`)}
>>>>>>> 78e1006 (Initial: presenton)
        variant="ghost"
        className="border border-white font-bold text-white rounded-[32px] transition-all duration-300 group"
      >
        <Play className="w-4 h-4 mr-1 stroke-white group-hover:stroke-black" />
        Present
      </Button>

      {/* Desktop Export Button with Popover */}

<<<<<<< HEAD
      <div style={{
        zIndex: 100
      }} className="hidden lg:block relative ">
        <Popover open={open} onOpenChange={setOpen} >
          <PopoverTrigger asChild>
            <Button className={`border py-5 text-[#5146E5] font-bold rounded-[32px] transition-all duration-500 hover:border hover:bg-[#5146E5] hover:text-white w-full ${mobile ? "" : "bg-white"}`}>
=======
      <div className="hidden lg:block">
        <Popover open={open} onOpenChange={setOpen}>
          <PopoverTrigger asChild>
            <Button className="bg-white border py-5 text-[#5146E5] font-bold rounded-[32px] transition-all duration-500 hover:border hover:bg-[#5146E5] hover:text-white w-full">
>>>>>>> 78e1006 (Initial: presenton)
              <SquareArrowOutUpRight className="w-4 h-4 mr-1" />
              Export
            </Button>
          </PopoverTrigger>
<<<<<<< HEAD
          <PopoverContent align="end" className="w-[250px] space-y-2 py-3 px-2 ">
            <ExportOptions mobile={false} />
=======
          <PopoverContent align="end" className="w-[250px] space-y-2 py-3 px-2">
            <ExportOptions />
>>>>>>> 78e1006 (Initial: presenton)
          </PopoverContent>
        </Popover>
      </div>

      {/* Mobile Export Section */}
      <div className="lg:hidden flex flex-col w-full">
<<<<<<< HEAD
        <ExportOptions mobile={true} />
=======
        <ExportOptions />
>>>>>>> 78e1006 (Initial: presenton)
      </div>
    </div>
  );

  return (
<<<<<<< HEAD
    <>
=======
    <div className="bg-[#5146E5] w-full shadow-lg sticky top-0 z-50">
>>>>>>> 78e1006 (Initial: presenton)
      <OverlayLoader
        show={showLoader}
        text="Exporting presentation..."
        showProgress={true}
        duration={40}
      />
<<<<<<< HEAD
      <div

        className="bg-[#5146E5] w-full shadow-lg sticky top-0 ">

        <Announcement />
        <Wrapper className="flex items-center justify-between py-1">
          <Link href="/dashboard" className="min-w-[162px]">
            <img
              className="h-16"
              src="/logo-white.png"
              alt="Presentation logo"
            />
          </Link>

          {/* Desktop Menu */}
          <div className="hidden lg:flex items-center gap-4 2xl:gap-6">
            {isStreaming && (
              <Loader2 className="animate-spin text-white font-bold w-6 h-6" />
            )}


            <MenuItems mobile={false} />
            <HeaderNav />
          </div>

          {/* Mobile Menu */}
          <div className="lg:hidden flex items-center gap-4">
            <HeaderNav />

          </div>
        </Wrapper>

      </div>
    </>
=======
      <Announcement />
      <Wrapper className="flex items-center justify-between py-2">
        <Link href="/" className="min-w-[162px]">
          <Image
            src="/logo-white.png"
            alt="Presentation logo"
            width={162}
            height={32}
            priority
          />
        </Link>

        {/* Desktop Menu */}
        <div className="hidden lg:flex items-center gap-4 2xl:gap-6">
          {isStreaming && (
            <Loader2 className="animate-spin text-white font-bold w-6 h-6" />
          )}
          <Select value={currentTheme} onValueChange={handleThemeSelect}>
            <SelectTrigger className="w-[160px] bg-[#6358fd] text-white border-none hover:bg-[#5146E5] transition-colors">
              <div className="flex items-center gap-2">
                <Palette className="w-4 h-4" />
                <span>Change Theme</span>
              </div>
            </SelectTrigger>
            <SelectContent className="w-[300px] p-0">
              <ThemeSelector
                onSelect={handleThemeSelect}
                selectedTheme={currentTheme}
              />
            </SelectContent>
          </Select>
          {/* Custom Theme Modal */}
          <Modal
            isOpen={showCustomThemeModal}
            onClose={() => setShowCustomThemeModal(false)}
            title="Custom Theme Colors"
          >
            <CustomThemeSettings
              onClose={() => setShowCustomThemeModal(false)}
              presentationId={presentation_id}
            />
          </Modal>
          <MenuItems />
          <UserAccount />
        </div>

        {/* Mobile Menu */}
        <div className="lg:hidden flex items-center gap-4">
          <UserAccount />
          <Sheet>
            <SheetTrigger asChild>
              <button className="text-white">
                <Menu className="h-6 w-6" />
              </button>
            </SheetTrigger>
            <SheetContent side="right" className="bg-[#5146E5] border-none p-4">
              <div className="flex flex-col gap-6 mt-10">
                <Select onValueChange={handleThemeSelect}>
                  <SelectTrigger className="w-full bg-[#6358fd] flex justify-center gap-2 text-white border-none">
                    <Palette className="w-4 h-4 mr-2" />
                    <SelectValue placeholder="Theme" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="light">Light Theme</SelectItem>
                    <SelectItem value="dark">Dark Theme</SelectItem>
                    <SelectItem value="royal_blue">Royal Blue Theme</SelectItem>
                    <SelectItem value="cream">Cream Theme</SelectItem>
                    <SelectItem value="dark_pink">Dark Pink Theme</SelectItem>
                    <SelectItem value="light_red">Light Red Theme</SelectItem>
                    <SelectItem value="faint_yellow">
                      Faint Yellow Theme
                    </SelectItem>
                    <SelectItem value="custom">Custom Theme</SelectItem>
                  </SelectContent>
                </Select>
                <MenuItems />
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </Wrapper>
    </div>
>>>>>>> 78e1006 (Initial: presenton)
  );
};

export default Header;
