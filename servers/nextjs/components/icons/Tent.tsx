import { cn } from '@/lib/utils'
import React from 'react'

const TentIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M18.337 9.088a.5.5 0 0 0-.129.695l1.168 1.574L7.4 27.5H4.5a.5.5 0 0 0 0 1h31a.5.5 0 0 0 0-1h-2.9L20.62 11.357l1.167-1.574a.5.5 0 0 0-.824-.566l-.965 1.301-.966-1.301a.5.5 0 0 0-.695-.129Zm2.48 12.036 3.591 5.088a.5.5 0 0 1-.817.576L20 21.7l-3.591 5.088a.5.5 0 0 1-.817-.576l3.591-5.088a1 1 0 0 1 1.634 0Z" fill="currentColor" />
        </svg>
    )
}

export default TentIcon 