import { cn } from '@/lib/utils'
import React from 'react'

const TreeIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M20 6a7 7 0 0 0-7 7v.427A7.5 7.5 0 0 0 15.5 28H19v4h-6a1 1 0 1 0 0 2h14a1 1 0 1 0 0-2h-6v-4h3.5A7.5 7.5 0 0 0 27 13.427V13a7 7 0 0 0-7-7Zm9.429 14.5a.5.5 0 0 1 .5.5c0 2.41-1.69 4.5-3.929 4.5a.5.5 0 0 1 0-1c1.548 0 2.929-1.492 2.929-3.5a.5.5 0 0 1 .5-.5Z" fill="currentColor" />
        </svg>
    )
}

export default TreeIcon 