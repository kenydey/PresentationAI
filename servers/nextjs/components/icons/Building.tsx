import { cn } from '@/lib/utils'
import React from 'react'

const BuildingIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg className={cn('', className)} xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox='0 0 40 40' width="40">
            <path d="M11 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v24a2 2 0 0 1-2 2h-4v-5a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v5h-4a2 2 0 0 1-2-2V8Zm8.5 7a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5h-1ZM19 9.5v2a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5ZM24.5 21a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5h-1Zm-.5-5.5v2a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5Zm.5-6.5a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5h-1ZM14 21.5v2a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5Zm.5-6.5a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5h-1ZM14 9.5v2a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5ZM19.5 21a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 0-.5-.5h-1Z" fill="currentColor" />
            <path d="M22 29v5h-4v-5h4Z" fill="currentColor" />
        </svg>
    )
}

export default BuildingIcon
