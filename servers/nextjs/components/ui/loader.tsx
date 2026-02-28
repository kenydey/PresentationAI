import { cn } from "@/lib/utils"

interface LoaderProps {
    text?: string
    className?: string
}

export const Loader = ({ text, className }: LoaderProps) => {
    return (
        <div className={cn("flex flex-col items-center justify-center", className)}>
            <div className="w-8 h-8 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin"></div>
            {text && (
<<<<<<< HEAD
                <p className="mt-4 text-white text-base font-inter font-semibold">{text}</p>
=======
                <p className="mt-4 text-white text-base font-satoshi font-semibold">{text}</p>
>>>>>>> 78e1006 (Initial: presenton)
            )}
        </div>
    )
} 