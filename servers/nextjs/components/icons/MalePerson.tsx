import { cn } from '@/lib/utils'
import React from 'react'

const MalePersonIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M17 7a3 3 0 1 1 6 0v1a3 3 0 0 1-6 0V7Z" fill="currentColor" />
            <path clip-rule="evenodd" d="m20 23-.858 11.153A2 2 0 0 1 17.148 36H16.5a.5.5 0 0 1-.5-.5V16.8l-1.168 5.608A2 2 0 0 1 12.874 24h-.76a.5.5 0 0 1-.489-.602l1.763-8.461A3.69 3.69 0 0 1 17 12h6a3.69 3.69 0 0 1 3.612 2.937l1.763 8.461a.5.5 0 0 1-.49.602h-.759a2 2 0 0 1-1.958-1.592L24 16.8v18.7a.5.5 0 0 1-.5.5h-.648a2 2 0 0 1-1.994-1.847L20 23Z" fill="currentColor" fillRule="evenodd" />
        </svg>
    )
}

export default MalePersonIcon 