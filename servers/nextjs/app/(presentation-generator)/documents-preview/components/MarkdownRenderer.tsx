"use client";

<<<<<<< HEAD
import React, { useState, useEffect } from "react";

import { marked } from "marked";

=======
import React from "react";

import { marked } from "marked";
>>>>>>> 78e1006 (Initial: presenton)
interface MarkdownRendererProps {
  content: string;
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
<<<<<<< HEAD
  const [markdownContent, setMarkdownContent] = useState<string>("");

  useEffect(() => {
    const parseMarkdown = async () => {
      try {
        const parsed = await marked.parse(content);
        setMarkdownContent(parsed);
      } catch (error) {
        console.error("Error parsing markdown:", error);
        setMarkdownContent("");
      }
    };

    parseMarkdown();
  }, [content]);

=======
  const markdownContent = marked.parse(content);
>>>>>>> 78e1006 (Initial: presenton)
  return (
    <div
      className="prose prose-slate max-w-none mb-10"
      dangerouslySetInnerHTML={{ __html: markdownContent }}
    />
  );
};

export default MarkdownRenderer;
