import Link from "next/link";
import Image from "next/image";
import Wrapper from "../Wrapper";

export default function Header() {
  return (
    <Wrapper className="py-4">
      <div className="flex justify-between items-center ">
        <div className="flex items-center w-[102px] h-[24px] md:w-[162px] md:h-[32px]">
          <a href="/">
            {" "}
            <Image
              src="/Logo.png"
              alt="Presentation  logo"
              width={162}
              height={32}
              priority
            />
          </a>
        </div>
        <div className="flex items-center gap-4">
          {/* <div className="hidden md:flex items-center gap-4">
          <Link href="/" className="text-[#000] text-center font-neue-montreal text-[16px] font-[400] leading-6 tracking-[0.64px]">Home</Link>
          <Link href="/" className="text-[#000] text-center font-neue-montreal text-[16px] font-[400] leading-6 tracking-[0.64px]">About</Link>
          <Link href="/" className="text-[#000] text-center font-neue-montreal text-[16px] font-[400] leading-6 tracking-[0.64px]">Contact</Link>
        </div> */}
          <Link
            href="/auth/login"
            className=" bg-gradient-to-r  text-xs md:text-base  from-[#9034EA] to-[#5146E5] text-white font-semibold md:py-3 md:px-8 py-2 px-4 rounded-full"
          >
            Get Started
          </Link>
        </div>
      </div>
    </Wrapper>
  );
}
