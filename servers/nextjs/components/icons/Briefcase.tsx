import { cn } from '@/lib/utils'
import React from 'react'

const BriefcaseIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M16 11v-1a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v1h8a2 2 0 0 1 2 2v4.125L29.767 20.3a3.5 3.5 0 0 1-2.1.7H21.5a1 1 0 0 0-1-1h-1a1 1 0 0 0-1 1h-6.167a3.5 3.5 0 0 1-2.1-.7L6 17.125V13a2 2 0 0 1 2-2h8Zm2-1v1h4v-1h-4Z" fill="currentColor" />
            <path d="M6 18.375V29a2 2 0 0 0 2 2h24a2 2 0 0 0 2-2V18.375L30.367 21.1a4.5 4.5 0 0 1-2.7.9H21.5v1a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-1h-6.167a4.5 4.5 0 0 1-2.7-.9L6 18.375Z" fill="currentColor" />
            <path d="M20.5 21h-1v2h1v-2Z" fill="currentColor" />
        </svg>
    )
}

export default BriefcaseIcon 