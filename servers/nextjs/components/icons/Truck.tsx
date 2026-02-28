import { cn } from '@/lib/utils'
import React from 'react'

const TruckIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M12 29a2 2 0 1 0 0-4 2 2 0 0 0 0 4ZM29 27a2 2 0 1 1-4 0 2 2 0 0 1 4 0Z" fill="currentColor">
            </path>
            <path d="M6 9a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v3h4a4 4 0 0 1 4 4v10a1 1 0 0 1-1 1h-2a4 4 0 0 1-8 0h-7a4 4 0 0 1-8 0H7a1 1 0 0 1-1-1V9Zm26 9v-2a2 2 0 0 0-2-2h-4v4h6Zm-17 9a3 3 0 1 0-6 0 3 3 0 0 0 6 0Zm12 3a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" fill="currentColor" />
        </svg>
    )
}

export default TruckIcon 