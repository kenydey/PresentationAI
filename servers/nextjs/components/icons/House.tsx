import { cn } from '@/lib/utils'
import React from 'react'

const HouseIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M30.276 20.2 19.746 9.434 9.214 20.2a1 1 0 0 1-1.43-1.398L18.673 7.67a1.5 1.5 0 0 1 2.145 0L24 10.924V8.5a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 .5.5v5.49l4.706 4.81a1 1 0 1 1-1.43 1.4Z" fill="currentColor" />
            <path d="M28.746 20.5v8a2 2 0 0 1-2 2h-4v-6a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v6h-4a2 2 0 0 1-2-2v-8l8.646-8.646a.5.5 0 0 1 .707 0l8.647 8.646Z" fill="currentColor" />
            <path d="M21.746 30.5v-6h-4v6h4Z" fill="currentColor" />
        </svg>
    )
}

export default HouseIcon 