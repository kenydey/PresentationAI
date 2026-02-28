import { cn } from '@/lib/utils'
import React from 'react'

const FemalePersonIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M20 4a3 3 0 0 0-3 3v1a3 3 0 1 0 6 0V7a3 3 0 0 0-3-3ZM17 17l-2.48 5.788A2 2 0 0 1 12.68 24h-.923a.5.5 0 0 1-.46-.697L14 17l.994-2.486A4 4 0 0 1 18.708 12h2.584a4 4 0 0 1 3.714 2.514L26 17l2.701 6.303a.5.5 0 0 1-.46.697h-.922a2 2 0 0 1-1.838-1.212L23 17l2.806 9.356a.5.5 0 0 1-.479.644h-1.386l-.657 8.538a.5.5 0 0 1-.498.462h-.112a2 2 0 0 1-1.999-1.923L20.404 27h-.808l-.272 7.077A2 2 0 0 1 17.325 36h-.112a.5.5 0 0 1-.498-.462L16.058 27h-1.386a.5.5 0 0 1-.479-.644L17 17Z" fill="currentColor" />
        </svg>
    )
}

export default FemalePersonIcon 