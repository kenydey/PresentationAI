/**
 * DocumentPreviewPage Component
<<<<<<< HEAD
 *
 * A component that displays and manages document previews for presentation generation.
 * Features:
 * - Document content preview with markdown support
 * - Sidebar navigation for documents
 * - Document content editing and saving
 * - Presentation generation workflow
 *
=======
 * 
 * A component that displays and manages document previews for presentation generation.
 * Features:
 * - Document content preview with markdown support
 * - Sidebar navigation for documents, reports, and images
 * - Document content editing and saving
 * - Tables and charts display
 * - Presentation generation workflow
 * 
>>>>>>> 78e1006 (Initial: presenton)
 * @component
 */

"use client";

<<<<<<< HEAD
=======
import styles from "../styles/main.module.css";
>>>>>>> 78e1006 (Initial: presenton)
import { useEffect, useState, useRef, useMemo } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import { OverlayLoader } from "@/components/ui/overlay-loader";
import { PresentationGenerationApi } from "../../services/api/presentation-generation";
<<<<<<< HEAD
import { setPresentationId } from "@/store/slices/presentationGeneration";
import { useDispatch, useSelector } from "react-redux";
import { useRouter, usePathname } from "next/navigation";
import { RootState } from "@/store/store";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import MarkdownRenderer from "./MarkdownRenderer";
import { getIconFromFile } from "../../utils/others";
import { ChevronRight, PanelRightOpen, X } from "lucide-react";
import ToolTip from "@/components/ToolTip";
import Header from "@/app/(presentation-generator)/dashboard/components/Header";
import { trackEvent, MixpanelEvent } from "@/utils/mixpanel";
=======
import { setTitles, setPresentationId } from "@/store/slices/presentationGeneration";
import { useDispatch, useSelector } from "react-redux";
import { useRouter } from "next/navigation";
import { RootState } from "@/store/store";
import { Button } from "@/components/ui/button";
import { toast } from "@/hooks/use-toast";
import Header from "@/app/dashboard/components/Header";
import MarkdownRenderer from "./MarkdownRenderer";
import { fetchTextFromURL } from "../../utils/download";
import { getIconFromFile, removeUUID } from "../../utils/others";
import { ChevronRight, PanelRightOpen, X } from "lucide-react";
import ToolTip from "@/components/ToolTip";
>>>>>>> 78e1006 (Initial: presenton)

// Types
interface LoadingState {
  message: string;
  show: boolean;
  duration: number;
  progress: boolean;
}

interface TextContents {
  [key: string]: string;
}

<<<<<<< HEAD
interface FileItem {
  name: string;
  file_path: string;
}
=======
>>>>>>> 78e1006 (Initial: presenton)

const DocumentsPreviewPage: React.FC = () => {
  // Hooks
  const dispatch = useDispatch();
  const router = useRouter();
<<<<<<< HEAD
  const pathname = usePathname();
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Redux state
  const { config, files } = useSelector(
=======
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Redux state
  const { config, reports, documents, images, charts, tables } = useSelector(
>>>>>>> 78e1006 (Initial: presenton)
    (state: RootState) => state.pptGenUpload
  );

  // Local state
  const [textContents, setTextContents] = useState<TextContents>({});
  const [selectedDocument, setSelectedDocument] = useState<string | null>(null);
<<<<<<< HEAD
  const [downloadingDocuments, setDownloadingDocuments] = useState<string[]>(
    []
  );
  const [isOpen, setIsOpen] = useState(true);
=======
  const [downloadingDocuments, setDownloadingDocuments] = useState<string[]>([]);
  const [isOpen, setIsOpen] = useState(true);
  const [changedDocuments, setChangedDocuments] = useState<string[]>([]);
>>>>>>> 78e1006 (Initial: presenton)
  const [showLoading, setShowLoading] = useState<LoadingState>({
    message: "",
    show: false,
    duration: 10,
    progress: false,
  });

<<<<<<< HEAD
  // Memoized computed values
  const fileItems: FileItem[] = useMemo(() => {
    if (!files || !Array.isArray(files) || files.length === 0) return [];
    return files
      .flat()
      .filter((item: any) => item && item.name && item.file_path);
  }, [files]);

  const documentKeys = useMemo(() => {
    return fileItems.map((file) => file.name);
  }, [fileItems]);
=======
  // Memoized values
  const reportKeys = useMemo(() => Object.keys(reports), [reports]);
  const documentKeys = useMemo(() => Object.keys(documents), [documents]);
  const imageKeys = useMemo(() => Object.keys(images), [images]);
  const allSources = useMemo(() => [...reportKeys, ...documentKeys, ...imageKeys], [reportKeys, documentKeys, imageKeys]);


>>>>>>> 78e1006 (Initial: presenton)

  const updateSelectedDocument = (value: string) => {
    setSelectedDocument(value);
    if (textareaRef.current) {
<<<<<<< HEAD
      textareaRef.current.value = textContents[value] || "";
    }
  };

  const readFile = async (filePath: string) => {
    const res = await fetch(`/api/read-file`, {
      method: "POST",
      body: JSON.stringify({ filePath }),
    });
    return res.json();
  };

  const maintainDocumentTexts = async () => {
    const newDocuments: string[] = [];
    const promises: Promise<{ content: string }>[] = [];

    // Process documents
    documentKeys.forEach((key: string) => {
      if (!(key in textContents)) {
        newDocuments.push(key);
        const fileItem = fileItems.find((item) => item.name === key);
        if (fileItem) {
          promises.push(readFile(fileItem.file_path));
        }
=======
      textareaRef.current.value = textContents[value] || '';
    }
  };

  const maintainDocumentTexts = async () => {

    const newDocuments: string[] = [];
    const promises: Promise<string>[] = [];

    // Process documents
    documentKeys.forEach(key => {
      if (!(key in textContents)) {
        newDocuments.push(key);
        promises.push(fetchTextFromURL(documents[key]));
      }
    });

    // Process reports
    reportKeys.forEach(key => {
      if (!(key in textContents)) {
        newDocuments.push(key);
        promises.push(fetchTextFromURL(reports[key]));
>>>>>>> 78e1006 (Initial: presenton)
      }
    });

    if (promises.length > 0) {
      setDownloadingDocuments(newDocuments);
<<<<<<< HEAD
      try {
        const results = await Promise.all(promises);
        setTextContents((prev) => {
          const newContents = { ...prev };
          newDocuments.forEach((key, index) => {
            newContents[key] = results[index].content || "";
          });
          return newContents;
        });
      } catch (error) {
        console.error("Error reading files:", error);
        toast.error("Failed to read document content");
      }
=======
      const results = await Promise.all(promises);
      setTextContents(prev => {
        const newContents = { ...prev };
        newDocuments.forEach((key, index) => {
          newContents[key] = results[index];
        });
        return newContents;
      });
>>>>>>> 78e1006 (Initial: presenton)
      setDownloadingDocuments([]);
    }
  };

<<<<<<< HEAD
=======


  const documentTablesAndCharts = () => {
    if (!selectedDocument) return [];

    const tablesList = tables[selectedDocument] || [];
    const chartsList = charts[selectedDocument] || [];
    return [...tablesList, ...chartsList];
  };

>>>>>>> 78e1006 (Initial: presenton)
  const handleCreatePresentation = async () => {
    try {
      setShowLoading({
        message: "Generating presentation outline...",
        show: true,
        duration: 40,
        progress: true,
      });

<<<<<<< HEAD
      const documentPaths = fileItems.map(
        (fileItem: FileItem) => fileItem.file_path
      );
      trackEvent(MixpanelEvent.DocumentsPreview_Create_Presentation_API_Call);
       const createResponse = await PresentationGenerationApi.createPresentation(
        {
          content: config?.prompt ?? "",
          n_slides: config?.slides ? parseInt(config.slides) : null,
          file_paths: documentPaths,
          language: config?.language ?? "",
          tone: config?.tone,
          verbosity: config?.verbosity,
          instructions: config?.instructions || null,
          include_table_of_contents: !!config?.includeTableOfContents,
          include_title_slide: !!config?.includeTitleSlide,
          web_search: !!config?.webSearch,
        }
      );

      dispatch(setPresentationId(createResponse.id));
      trackEvent(MixpanelEvent.Navigation, { from: pathname, to: "/outline" });
      router.replace("/outline");
    } catch (error: any) {
      console.error("Error in radar presentation creation:", error);
      toast.error("Error", {
        description: error.message || "Error in radar presentation creation.",
      });
      setShowLoading({
        message: "Error in radar presentation creation.",
=======
      const documentPaths = documentKeys.map(key => documents[key]);

      const createResponse = await PresentationGenerationApi.getQuestions({
        prompt: config?.prompt ?? "",
        n_slides: config?.slides ? parseInt(config.slides) : null,
        documents: documentPaths,
        images: imageKeys,
        research_reports: [reports['research_report_content']],
        language: config?.language ?? "",
        sources: allSources,
      });

      try {
        const titlePromise = await PresentationGenerationApi.titleGeneration({
          presentation_id: createResponse.id,
        });

        dispatch(setPresentationId(titlePromise.id));
        dispatch(setTitles(titlePromise.titles));

        setShowLoading({
          message: "",
          show: false,
          duration: 0,
          progress: false,
        });

        router.push("/theme");
      } catch (error) {
        console.error("Error in title generation:", error);
        toast({
          title: "Error in title generation.",
          description: "Please try again.",
          variant: "destructive",
        });
      }
    } catch (error) {
      console.error("Error in presentation creation:", error);
      toast({
        title: "Error in presentation creation.",
        description: "Please try again.",
        variant: "destructive",
      });
      setShowLoading({
        message: "Error in presentation creation.",
>>>>>>> 78e1006 (Initial: presenton)
        show: true,
        duration: 10,
        progress: false,
      });
    } finally {
      setShowLoading({
        message: "",
        show: false,
        duration: 10,
        progress: false,
      });
    }
  };

  // Effects
  useEffect(() => {
<<<<<<< HEAD
    if (documentKeys.length > 0) {
      setSelectedDocument(documentKeys[0]);
      maintainDocumentTexts();
    }
  }, [documentKeys]);
=======
    if (allSources.length > 0) {
      setSelectedDocument(allSources[0]);
      maintainDocumentTexts();
    }
  }, [allSources]);
>>>>>>> 78e1006 (Initial: presenton)

  // Render helpers
  const renderDocumentContent = () => {
    if (!selectedDocument) return null;

    const isDocument = documentKeys.includes(selectedDocument);
<<<<<<< HEAD

    if (!isDocument) return null;

    return (
      <div className="h-full mr-4">
        <div className="overflow-y-auto custom_scrollbar h-full">
=======
    const isReport = reportKeys.includes(selectedDocument);
    const hasTablesAndCharts = documentTablesAndCharts().length > 0;

    if (!isDocument && !isReport) return null;

    return (
      <div className="h-full mr-4">
        <div className={`overflow-y-auto custom_scrollbar ${hasTablesAndCharts ? "h-[calc(100vh-300px)]" : "h-full"
          }`}>
>>>>>>> 78e1006 (Initial: presenton)
          <div className="h-full w-full max-w-full flex flex-col mb-5">
            <h1 className="text-2xl font-medium mb-5">Content:</h1>
            {downloadingDocuments.includes(selectedDocument) ? (
              <Skeleton className="w-full h-full" />
            ) : (
<<<<<<< HEAD
              <MarkdownRenderer
                content={textContents[selectedDocument] || ""}
              />
            )}
          </div>
        </div>
=======
              <MarkdownRenderer content={textContents[selectedDocument] || ""} />
            )}
          </div>
        </div>
        {hasTablesAndCharts && (
          <div className="py-4">
            <h1 className="text-2xl font-medium mb-5">Tables And Charts</h1>
            {documentTablesAndCharts().map((item, index) => (
              <div
                key={index}
                className="w-full border rounded-lg p-4 my-4 bg-white shadow-sm"
              >
                {item.markdown && (
                  <MarkdownRenderer
                    key={selectedDocument}
                    content={item.markdown}
                  />
                )}
              </div>
            ))}
          </div>
        )}
>>>>>>> 78e1006 (Initial: presenton)
      </div>
    );
  };

  const renderSidebar = () => {
    if (!isOpen) return null;

    return (
<<<<<<< HEAD
      <div className={`border-r border-gray-200 fixed xl:relative w-full z-50 xl:z-auto
        transition-all duration-300 bg-white ease-in-out max-w-[200px] md:max-w-[300px] h-[85vh] rounded-md p-5`}>
=======
      <div className={`${styles.sidebar} fixed xl:relative w-full z-50 xl:z-auto
        transition-all duration-300 ease-in-out max-w-[200px] md:max-w-[300px] h-[85vh] rounded-md p-5`}>
>>>>>>> 78e1006 (Initial: presenton)
        <X
          onClick={() => setIsOpen(false)}
          className="text-black mb-4 ml-auto mr-0 cursor-pointer hover:text-gray-600"
          size={20}
        />

<<<<<<< HEAD
=======
        {reportKeys.length > 0 && (
          <div
            onClick={() => updateSelectedDocument(reportKeys[0])}
            className={`${selectedDocument === reportKeys[0]
              ? styles.selected_border
              : styles.unselected_border
              } ${styles.report_icon_box} flex justify-center items-center rounded-lg w-full h-32 cursor-pointer`}
          >
            <div>
              <img
                className="mx-auto h-20"
                src="/report.png"
                alt="Research Report"
              />
              <p className="text-sm mt-2 text-[#2E2E2E]">Research Report</p>
            </div>
          </div>
        )}

>>>>>>> 78e1006 (Initial: presenton)
        {documentKeys.length > 0 && (
          <div className="mt-8">
            <p className="text-xs mt-2 text-[#2E2E2E] opacity-70">DOCUMENTS</p>
            <div className="flex flex-col gap-2 mt-6">
<<<<<<< HEAD
              {documentKeys.map((key: string) => (
                <div
                  key={key}
                  onClick={() => updateSelectedDocument(key)}
                  className={`${
                    selectedDocument === key ? "border border-blue-500" : ""
                  } flex p-2 rounded-sm gap-2 items-center cursor-pointer`}
=======
              {documentKeys.map((key) => (
                <div
                  key={key}
                  onClick={() => updateSelectedDocument(key)}
                  className={`${selectedDocument === key ? styles.selected_border : ""
                    } flex p-2 rounded-sm gap-2 items-center cursor-pointer`}
>>>>>>> 78e1006 (Initial: presenton)
                >
                  <img
                    className="h-6 w-6 border border-gray-200"
                    src={getIconFromFile(key)}
                    alt="Document icon"
                  />
                  <span className="text-sm h-6 text-[#2E2E2E] overflow-hidden">
<<<<<<< HEAD
                    {key.split("/").pop() ?? "file.txt"}
=======
                    {removeUUID(key.split("/").pop() ?? "file.txt")}
>>>>>>> 78e1006 (Initial: presenton)
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
<<<<<<< HEAD
=======

        {imageKeys.length > 0 && (
          <div className="mt-8">
            <p className="text-xs mt-2 text-[#2E2E2E] opacity-70">IMAGES</p>
            <div className="flex flex-col gap-2 mt-6">
              {imageKeys.map((key) => (
                <div
                  key={key}
                  onClick={() => updateSelectedDocument(key)}
                  className="cursor-pointer"
                >
                  <img
                    className={`${selectedDocument === key
                      ? styles.selected_border
                      : styles.unselected_border
                      } ${styles.uploaded_images} rounded-lg h-24 w-full border border-gray-200`}
                    src={images[key]}
                    alt="Uploaded image"
                  />
                </div>
              ))}
            </div>
          </div>
        )}
>>>>>>> 78e1006 (Initial: presenton)
      </div>
    );
  };

  return (
<<<<<<< HEAD
    <div className={`bg-white/90 min-h-screen flex flex-col w-full`}>
=======
    <div className={`${styles.wrapper} min-h-screen flex flex-col w-full`}>
>>>>>>> 78e1006 (Initial: presenton)
      <OverlayLoader
        show={showLoading.show}
        text={showLoading.message}
        showProgress={showLoading.progress}
        duration={showLoading.duration}
      />
<<<<<<< HEAD
      <Header />
      <div className="flex mt-6 gap-4 font-instrument_sans">
=======

      <Header />
      <div className="flex mt-6 gap-4">
>>>>>>> 78e1006 (Initial: presenton)
        {!isOpen && (
          <div className="fixed left-4 top-1/2 -translate-y-1/2 z-50">
            <ToolTip content="Open Panel">
              <Button
                onClick={() => setIsOpen(true)}
                className="bg-[#5146E5] text-white p-3 shadow-lg"
              >
                <PanelRightOpen className="text-white" size={20} />
              </Button>
            </ToolTip>
          </div>
        )}

        {renderSidebar()}

        <div className="bg-white w-full mx-2 sm:mx-4 h-[calc(100vh-100px)] custom_scrollbar rounded-md overflow-y-auto py-6 pl-6">
          {renderDocumentContent()}
        </div>

        <div className="fixed bottom-5 right-5">
          <Button
            onClick={handleCreatePresentation}
            className="flex items-center gap-2 px-8 py-6 rounded-sm text-md bg-[#5146E5] hover:bg-[#5146E5]/90"
          >
            <span className="text-white font-semibold">Next</span>
            <ChevronRight />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default DocumentsPreviewPage;
