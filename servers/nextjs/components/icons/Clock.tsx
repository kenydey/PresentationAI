import { cn } from '@/lib/utils'
import React from 'react'

const ClockIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M31 20c0 6.075-4.925 11-11 11S9 26.075 9 20 13.925 9 20 9s11 4.925 11 11Zm-11.5.207 5.803 5.803a.5.5 0 1 0 .707-.707l-5.51-5.51V12a.5.5 0 0 0-1 0v8.207Z" fill="currentColor" />
            <path d="M34 20c0 7.732-6.268 14-14 14S6 27.732 6 20 12.268 6 20 6s14 6.268 14 14Zm-2 0c0-6.627-5.373-12-12-12S8 13.373 8 20s5.373 12 12 12 12-5.373 12-12Z" fill="currentColor" />
        </svg>
    )
}

export default ClockIcon 