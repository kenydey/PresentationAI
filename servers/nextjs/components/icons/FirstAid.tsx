import { cn } from '@/lib/utils'
import React from 'react'

const FirstAidIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M21.5 16.5a.5.5 0 0 0-.5-.5h-2a.5.5 0 0 0-.5.5v2a.5.5 0 0 1-.5.5h-2a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5h2a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 .5.5h2a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 1 .5-.5h2a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5h-2a.5.5 0 0 1-.5-.5v-2Z" fill="currentColor" />
            <path d="M16 9v1H7a2 2 0 0 0-2 2v17a2 2 0 0 0 2 2h26a2 2 0 0 0 2-2V12a2 2 0 0 0-2-2h-9V9a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2Zm6 0v1h-4V9h4ZM9.5 12a.5.5 0 0 1 .5.5v16a.5.5 0 0 1-1 0v-16a.5.5 0 0 1 .5-.5Zm20.5.5a.5.5 0 0 1 1 0v16a.5.5 0 0 1-1 0v-16ZM21 15a1.5 1.5 0 0 1 1.5 1.5V18H24a1.5 1.5 0 0 1 1.5 1.5v2A1.5 1.5 0 0 1 24 23h-1.5v1.5A1.5 1.5 0 0 1 21 26h-2a1.5 1.5 0 0 1-1.5-1.5V23H16a1.5 1.5 0 0 1-1.5-1.5v-2A1.5 1.5 0 0 1 16 18h1.5v-1.5A1.5 1.5 0 0 1 19 15h2Z" fill="currentColor" />
        </svg>
    )
}

export default FirstAidIcon 