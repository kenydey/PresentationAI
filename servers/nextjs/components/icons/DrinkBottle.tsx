import { cn } from '@/lib/utils'
import React from 'react'

const DrinkBottleIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M14 18h12v16a2 2 0 0 1-2 2h-8a2 2 0 0 1-2-2V18ZM14 12a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v5H14v-5ZM17 5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1V5Z" fill="currentColor" />
        </svg>
    )
}

export default DrinkBottleIcon 