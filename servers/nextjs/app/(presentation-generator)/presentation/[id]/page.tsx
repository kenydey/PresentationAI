import React from "react";
import PresentationPage from "../components/PresentationPage";
import { Metadata } from "next";
import { FooterProvider } from "../../context/footerContext";

export const metadata: Metadata = {
  title: "Presentation | PresentOn",
  description:
    "View your presentation in full screen mode edit content and download your presentation. Enjoy the seamless experience of presenting your data with ease.",
  alternates: {
    canonical: "https://presenton.ai/presentation",
  },
  keywords: [
    "presentation viewer",
    "AI presentations",
    "data visualization",
    "automatic presentation maker",
    "professional slides",
    "data-driven presentations",
    "document to presentation",
    "presentation automation",
    "smart presentation tool",
    "business presentations",
    "slide editor",
    "presentation software",
    "AI-powered slides",
    "real-time collaboration",
    "presentation templates",
  ],
};

const page = ({ params }: { params: { id: string } }) => {
  return (
    <FooterProvider>
      <PresentationPage presentation_id={params.id} />
    </FooterProvider>
  );
};
export default page;
