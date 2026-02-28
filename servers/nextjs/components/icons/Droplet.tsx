import { cn } from '@/lib/utils'
import React from 'react'

const DropletIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M20 34c5.727 0 10.37-4.864 10.37-10.866 0-5.027-7.277-14.022-9.64-16.81a.951.951 0 0 0-1.461 0c-2.362 2.788-9.64 11.783-9.64 16.81C9.63 29.136 14.272 34 20 34Zm8.514-10.866c0 5.198-3.983 9.102-8.514 9.102a.5.5 0 1 1 0-1c3.942 0 7.514-3.419 7.514-8.102a.5.5 0 1 1 1 0Z" fill="currentColor" />
        </svg>
    )
}

export default DropletIcon 