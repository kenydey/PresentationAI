import { cn } from '@/lib/utils'
import React from 'react'

const CarIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M12 25.5a2 2 0 1 0-4 0 2 2 0 0 0 4 0ZM29 27.5a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z" fill="currentColor" />
            <path d="M10.465 9a5 5 0 0 0-4.682 3.244L4 17v8a1 1 0 0 0 1 1h1.03a4 4 0 0 0 7.94 0h11.06a4 4 0 0 0 7.94 0H35a1 1 0 0 0 1-1v-4a4 4 0 0 0-4-4h-4l-1.783-4.756A5 5 0 0 0 21.535 9h-11.07ZM10 28.5a3 3 0 1 1 0-6 3 3 0 0 1 0 6Zm22-3a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM16 11v6H6.134l1.522-4.053A3 3 0 0 1 10.465 11H16Zm2 0h3.535a3 3 0 0 1 2.809 1.947L25.86 17H18v-6Z" fill="currentColor" />
        </svg>
    )
}

export default CarIcon 