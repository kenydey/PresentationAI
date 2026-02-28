import { cn } from '@/lib/utils'
import React from 'react'

const MortarboardIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M5.246 17.925c-.826-.34-.826-1.51 0-1.85l14.373-5.918a1 1 0 0 1 .762 0l14.373 5.918c.826.34.826 1.51 0 1.85l-2.38.98v3.147a1 1 0 0 1 0 1.733v.134l.638 1.276a.5.5 0 0 1-.447.724h-1.382a.5.5 0 0 1-.448-.724l.639-1.276v-.134a1 1 0 0 1 0-1.733v-2.735L20.38 23.843a1 1 0 0 1-.762 0L5.246 17.925Z" fill="currentColor" />
            <path d="M10 20.964V28c0 1.105 4.477 2 10 2s10-.895 10-2v-7.036l-9.238 3.804a2 2 0 0 1-1.523 0L10 20.964Z" fill="currentColor" />
        </svg>
    )
}

export default MortarboardIcon 