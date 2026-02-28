import { cn } from '@/lib/utils'
import React from 'react'

const CupIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M25.207 31h-9.414l-1.56-19h12.534l-1.56 18.99V31Z" fill="currentColor" />
            <path d="M12.074 6a1 1 0 0 0-.998 1.071l1.725 24.143A3 3 0 0 0 15.793 34h9.414a3 3 0 0 0 2.992-2.786L29.923 7.07A1 1 0 0 0 28.927 6H12.074Zm2.16 5h12.533a1 1 0 0 1 .996 1.082l-1.559 18.99a1 1 0 0 1-.997.928h-9.414a1 1 0 0 1-.997-.929l-1.56-18.99A1 1 0 0 1 14.234 11Z" fill="currentColor" />
        </svg>
    )
}

export default CupIcon 