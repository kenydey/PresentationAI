import type { Metadata } from "next";
import localFont from "next/font/local";
<<<<<<< HEAD
import { Roboto, Instrument_Sans } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";
import MixpanelInitializer from "./MixpanelInitializer";
import { Toaster } from "@/components/ui/sonner";
=======
import { Fraunces, Montserrat, Inria_Serif } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";
import { Toaster } from "@/components/ui/toaster";
import Script from "next/script";
import { GoogleTagManager } from "@next/third-parties/google";

const fraunces = Fraunces({
  subsets: ["latin"],
  weight: ["400"],
  variable: "--font-fraunces",
});
const montserrat = Montserrat({
  subsets: ["latin"],
  weight: ["400"],
  variable: "--font-montserrat",
});
const inria_serif = Inria_Serif({
  subsets: ["latin"],
  weight: ["400"],
  variable: "--font-inria-serif",
});

>>>>>>> 78e1006 (Initial: presenton)
const inter = localFont({
  src: [
    {
      path: "./fonts/Inter.ttf",
      weight: "400",
      style: "normal",
    },
  ],
  variable: "--font-inter",
});

<<<<<<< HEAD
const instrument_sans = Instrument_Sans({
  subsets: ["latin"],
  weight: ["400"],
  variable: "--font-instrument-sans",
});

const roboto = Roboto({
  subsets: ["latin"],
  weight: ["400"],
  variable: "--font-roboto",
});


export const metadata: Metadata = {
  metadataBase: new URL("https://presenton.ai"),
  title: "Presenton - Open Source AI presentation generator",
  description:
    "Open-source AI presentation generator with custom layouts, multi-model support (OpenAI, Gemini, Ollama), and PDF/PPTX export. A free Gamma alternative.",
  keywords: [
    "AI presentation generator",
=======
// Neue Montreal fonts
const neueMontreal = localFont({
  src: [
    {
      path: "./fonts/NeueMontreal/NeueMontreal-Regular.otf",
      weight: "400",
      style: "normal",
    },
    {
      path: "./fonts/NeueMontreal/NeueMontreal-Bold.otf",
      weight: "700",
      style: "normal",
    },
    {
      path: "./fonts/NeueMontreal/NeueMontreal-Light.otf",
      weight: "300",
      style: "normal",
    },
    {
      path: "./fonts/NeueMontreal/NeueMontreal-Medium.otf",
      weight: "500",
      style: "normal",
    },
    {
      path: "./fonts/NeueMontreal/NeueMontreal-Italic.otf",
      weight: "400",
      style: "italic",
    },
  ],
  variable: "--font-neue-montreal",
});

// Satoshi fonts
const satoshi = localFont({
  src: [
    {
      path: "./fonts/Satoshi/Satoshi-Regular.otf",
      weight: "400",
      style: "normal",
    },
    {
      path: "./fonts/Satoshi/Satoshi-Bold.otf",
      weight: "700",
      style: "normal",
    },
    {
      path: "./fonts/Satoshi/Satoshi-Light.otf",
      weight: "300",
      style: "normal",
    },
    {
      path: "./fonts/Satoshi/Satoshi-Medium.otf",
      weight: "500",
      style: "normal",
    },
    {
      path: "./fonts/Satoshi/Satoshi-Black.otf",
      weight: "900",
      style: "normal",
    },
  ],
  variable: "--font-satoshi",
});

// Switzer fonts
const switzer = localFont({
  src: [
    {
      path: "./fonts/Switzer/Switzer-Regular.otf",
      weight: "400",
      style: "normal",
    },
    {
      path: "./fonts/Switzer/Switzer-Bold.otf",
      weight: "700",
      style: "normal",
    },
    {
      path: "./fonts/Switzer/Switzer-Light.otf",
      weight: "300",
      style: "normal",
    },
    {
      path: "./fonts/Switzer/Switzer-Medium.otf",
      weight: "500",
      style: "normal",
    },
    {
      path: "./fonts/Switzer/Switzer-Black.otf",
      weight: "900",
      style: "normal",
    },
  ],
  variable: "--font-switzer",
});

export const metadata: Metadata = {
  metadataBase: new URL("https://presenton.ai"),
  title: "Presenton.ai - AI Presentation Maker for Data Storytelling",
  description:
    "Turn complex data into stunning, interactive presentations with Presenton.ai. Create professional slides from reports and analytics in minutes. Try now!",
  keywords: [
    "AI presentation maker",
>>>>>>> 78e1006 (Initial: presenton)
    "data storytelling",
    "data visualization tool",
    "AI data presentation",
    "presentation generator",
    "data to presentation",
    "interactive presentations",
    "professional slides",
  ],
  openGraph: {
<<<<<<< HEAD
    title: "Presenton - Open Source AI presentation generator",
    description:
      "Open-source AI presentation generator with custom layouts, multi-model support (OpenAI, Gemini, Ollama), and PDF/PPTX export. A free Gamma alternative.",
    url: "https://presenton.ai",
    siteName: "Presenton",
=======
    title: "Presenton.ai - AI-Powered Data Presentations",
    description:
      "Transform data into engaging presentations effortlessly with Presenton.ai, your go-to AI tool for stunning slides and data storytelling.",
    url: "https://presenton.ai",
    siteName: "Presenton.ai",
>>>>>>> 78e1006 (Initial: presenton)
    images: [
      {
        url: "https://presenton.ai/presenton-feature-graphics.png",
        width: 1200,
        height: 630,
<<<<<<< HEAD
        alt: "Presenton Logo",
=======
        alt: "Presenton.ai Logo",
>>>>>>> 78e1006 (Initial: presenton)
      },
    ],
    type: "website",
    locale: "en_US",
  },
  alternates: {
    canonical: "https://presenton.ai",
  },
  twitter: {
    card: "summary_large_image",
<<<<<<< HEAD
    title: "Presenton - Open Source AI presentation generator",
    description:
      "Open-source AI presentation generator with custom layouts, multi-model support (OpenAI, Gemini, Ollama), and PDF/PPTX export. A free Gamma alternative.",
=======
    title: "Presenton.ai - AI Presentation Maker for Data Storytelling",
    description:
      "Create stunning presentations from data with Presenton.ai. Simplify reports and analytics into interactive slides fast!",
>>>>>>> 78e1006 (Initial: presenton)
    images: ["https://presenton.ai/presenton-feature-graphics.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
<<<<<<< HEAD

  return (
    <html lang="en">
      <body
        className={`${inter.variable} ${roboto.variable} ${instrument_sans.variable} antialiased`}
      >
        <Providers>
          <MixpanelInitializer>

            {children}

          </MixpanelInitializer>
        </Providers>
        <Toaster position="top-center" />
=======
  return (
    <html lang="en">
      <body
        className={`$ ${neueMontreal.variable} ${satoshi.variable} ${switzer.variable} ${inter.variable} ${fraunces.variable} ${montserrat.variable} ${inria_serif.variable} antialiased`}
      >
        <Providers>{children}</Providers>
        <Toaster />
>>>>>>> 78e1006 (Initial: presenton)
      </body>
    </html>
  );
}
