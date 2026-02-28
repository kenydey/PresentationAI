import { cn } from '@/lib/utils'
import React from 'react'

const LaptopIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M30 12H10v12h20V12Z" fill="currentColor" />
            <path d="M9 9a2 2 0 0 0-2 2v16h26V11a2 2 0 0 0-2-2H9Zm.917 2h20.166c.507 0 .917.392.917.875V25H9V11.875c0-.483.41-.875.917-.875ZM4 29v-1h12a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1h12v1a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1Z" fill="currentColor" />
        </svg>
    )
}

export default LaptopIcon 