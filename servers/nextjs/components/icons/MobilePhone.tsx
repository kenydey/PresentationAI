import { cn } from '@/lib/utils'
import React from 'react'

const MobilePhoneIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M14 5a2 2 0 0 0-2 2v26a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2H14Zm5.5 2h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1 0-1Zm-2.5.5a.5.5 0 1 1 1 0 .5.5 0 0 1-1 0ZM18.5 32h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1 0-1Z" fill="currentColor" />
        </svg>
    )
}

export default MobilePhoneIcon 