import { cn } from "@/lib/utils"
import { Loader } from "./loader"
import { ProgressBar } from "./progress-bar"
<<<<<<< HEAD
import { useEffect, useState } from "react"

=======
import { useEffect, useRef } from "react"
import anime from "animejs"
import Image from "next/image"
>>>>>>> 78e1006 (Initial: presenton)
interface OverlayLoaderProps {
    text?: string
    className?: string
    show: boolean
    showProgress?: boolean
    duration?: number
    extra_info?: string
    onProgressComplete?: () => void
}

export const OverlayLoader = ({
    text,
    className,
    show,
    showProgress = false,
    duration = 10,
    onProgressComplete,
    extra_info
}: OverlayLoaderProps) => {
<<<<<<< HEAD
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        if (show) {
            setIsVisible(true);
        } else {
            setIsVisible(false);
=======
    const overlayRef = useRef<HTMLDivElement>(null);
    const contentRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (show && overlayRef.current && contentRef.current) {
            // Animate overlay fade in
            anime({
                targets: overlayRef.current,
                opacity: [0, 1],
                duration: 300,
                easing: 'easeInOutQuad'
            });

            // Animate content scale and fade in
            anime({
                targets: contentRef.current,
                scale: [0.9, 1],
                opacity: [0, 1],
                duration: 400,
                easing: 'easeOutQuad'
            });
>>>>>>> 78e1006 (Initial: presenton)
        }
    }, [show]);

    if (!show) return null;

    return (
        <div
<<<<<<< HEAD
            style={{
                zIndex: 1000
            }}
            className={cn(
                "fixed inset-0 bg-black/70 z-50 flex items-center justify-center transition-opacity duration-300",
                isVisible ? "opacity-100" : "opacity-0"
            )}
        >
            <div
                className={cn(
                    "flex flex-col items-center justify-center px-6  pt-0 pb-8 rounded-xl bg-[#030303] shadow-2xl",
                    "min-w-[280px] sm:min-w-[330px] border border-white/10 transition-all duration-400 ease-out",
                    isVisible ? "opacity-100 scale-100" : "opacity-0 scale-90",
=======
            ref={overlayRef}
            className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center opacity-0"
        >
            <div
                ref={contentRef}
                className={cn(
                    "flex flex-col items-center justify-center px-6  pt-0 pb-8 rounded-xl bg-[#030303] shadow-2xl",
                    "min-w-[280px] sm:min-w-[330px] border border-white/10 opacity-0",
>>>>>>> 78e1006 (Initial: presenton)
                    className
                )}

            >
                <img loading="eager" src={'/loading.gif'} alt="loading" width={250} height={250} />
                {showProgress ? (
                    <div className="w-full space-y-6 pt-4">
                        <ProgressBar
                            duration={duration}
                            onComplete={onProgressComplete}
                        />
                        {text && (
                            <div className="space-y-1">
<<<<<<< HEAD
                                <p className="text-white text-base text-center font-semibold font-inter">
                                    {text}
                                </p>
                                {extra_info && <p className="text-white/80 text-xs text-center font-semibold font-inter">{extra_info}</p>}
=======
                                <p className="text-white text-base text-center font-semibold font-satoshi">
                                    {text}
                                </p>
                                {extra_info && <p className="text-white/80 text-xs text-center font-semibold font-satoshi">{extra_info}</p>}
>>>>>>> 78e1006 (Initial: presenton)
                            </div>
                        )}
                    </div>
                ) : (
                    <>
<<<<<<< HEAD
                        <p className="text-white text-base text-center font-semibold font-inter">
                            {text}
                        </p>
                        {extra_info && <p className="text-white/80 text-xs text-center font-semibold font-inter">{extra_info}</p>}
                    </>

=======
                        <p className="text-white text-base text-center font-semibold font-satoshi">
                            {text}
                        </p>
                        {extra_info && <p className="text-white/80 text-xs text-center font-semibold font-satoshi">{extra_info}</p>}
                    </>
                    // <div className="flex flex-col items-center gap-4">
                    //     <div className="relative">
                    //         <div className="absolute inset-0 bg-gradient-to-r from-[#9034EA] to-[#5146E5] blur-xl opacity-20" />
                    //         <Loader text={text} />
                    //     </div>

                    // </div>
>>>>>>> 78e1006 (Initial: presenton)
                )}
            </div>
        </div>
    )
} 