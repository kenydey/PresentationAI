import { cn } from '@/lib/utils'
import React from 'react'

const SpannerIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M29.217 28.717a1 1 0 1 0-2 0 1 1 0 0 0 2 0Z" fill="currentColor" />
            <path d="M21.101 15.945a7.997 7.997 0 0 0-2.071-7.729 7.979 7.979 0 0 0-6.018-2.335c-.77.035-1.03.945-.485 1.49l3.944 3.944a1 1 0 0 1 .242 1.023l-1.06 3.182a1 1 0 0 1-.633.632l-3.182 1.061a1 1 0 0 1-1.023-.242L6.87 13.027c-.544-.544-1.454-.285-1.489.485a7.98 7.98 0 0 0 2.335 6.018 7.997 7.997 0 0 0 7.729 2.071l9.858 9.86a4 4 0 0 0 5.657-5.658l-9.859-9.858Zm5.116 12.772a2 2 0 1 1 4 0 2 2 0 0 1-4 0Z" fill="currentColor" />
        </svg>
    )
}

export default SpannerIcon 