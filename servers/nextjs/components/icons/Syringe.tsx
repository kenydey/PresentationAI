import { cn } from '@/lib/utils'
import React from 'react'

const SyringeIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M15.5 4a.5.5 0 0 0 0 1H17v3h-2.5a.5.5 0 0 0 0 1H16v2h3.5a.5.5 0 0 1 0 1H16v2h3.5a.5.5 0 0 1 0 1H16v2h3.5a.5.5 0 0 1 0 1H16v9a4 4 0 0 0 3.5 3.97v3.794c0 .155.036.308.106.447l.305.61a.1.1 0 0 0 .178 0l.305-.61a.999.999 0 0 0 .106-.447v-3.795A4 4 0 0 0 24 27V9h1.5a.5.5 0 0 0 0-1H23V5h1.5a.5.5 0 0 0 0-1h-9Z" fill="currentColor" />
        </svg>
    )
}

export default SyringeIcon 