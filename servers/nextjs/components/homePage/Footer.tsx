import React from "react";
import Link from "next/link";
import Wrapper from "@/components/Wrapper";

interface FooterLink {
  label: string;
  href: string;
}

interface FooterSection {
  title: string;
  links: FooterLink[];
}

const footerSections: FooterSection[] = [
  {
    title: "Main Menu",
    links: [
      // { label: "About Us", href: "/about" },
      // { label: "Templates", href: "/templates" },
      { label: "Blogs", href: "/blogs" },
      { label: "Pricing", href: "#pricing" },
      // { label: "Enterprise", href: "/enterprise" },
      { label: "Contact Us", href: "/contact" },
    ],
  },
  {
    title: "Our Products",
    links: [
      { label: "Presentation Generator", href: "/upload" },
      { label: "Presentation-to-video", href: "/editor" },
      // { label: "Presentation-to-ppt", href: "/product-3" },
    ],
  },
  // {
  //     title: "Solutions",
  //     links: [
  //         { label: "Solution 1", href: "/solution-1" },
  //         { label: "Solution 2", href: "/solution-2" },
  //         { label: "Solution 3", href: "/solution-3" },
  //     ]
  // },
  {
    title: "Other Links",
    links: [
      { label: "FAQ", href: "#faq" },
      { label: "Terms & Conditions", href: "/terms-and-conditions" },
      { label: "Privacy Policy", href: "/privacy-policy" },
      // { label: "Cookies Policy", href: "/cookies-policy" },
    ],
  },
];

const Footer = () => {
  return (
    <footer className="bg-black text-white pt-20 pb-10">
      <Wrapper>
        <div className="flex flex-col lg:flex-row items-start justify-between gap-10">
          {/* Logo and Description Section */}
          <div className="lg:w-[30%] space-y-6">
            <Link href="/" className="inline-block">
              <img
                src="/logo-white.png"
                alt="Presenton.ai Logo"
                className="w-[204px] h-[48px] object-cover"
              />
            </Link>
            <p className="text-white font-normal font-satoshi">
              No more struggling with slides. Just drop your content and let
              your AI buddy craft beautiful, ready-to-share presentations for
              work, study, or business — in minutes.
            </p>
          </div>

          {/* Links Sections */}
          <div
            style={{
              gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))",
            }}
            className="w-full lg:w-[60%] grid  gap-10"
          >
            {footerSections.map((section) => (
              <div key={section.title}>
                <h3 className="text-lg font-switzer font-bold mb-6">
                  {section.title}{" "}
                </h3>
                <ul className="space-y-4">
                  {section.links.map((link) => (
                    <li key={link.label}>
                      <Link
                        href={link.href}
                        className="text-gray-400 hover:text-white transition-colors font-satoshi"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Copyright Section */}
        <div className="mt-16 pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-center    items-center gap-4">
          <p className="text-gray-400 text-sm font-satoshi">
            Copyright {new Date().getFullYear()} Presenton. All Right Reserved.
          </p>
        </div>
      </Wrapper>
    </footer>
  );
};

export default Footer;
