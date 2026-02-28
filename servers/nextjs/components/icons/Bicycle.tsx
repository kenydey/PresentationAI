import { cn } from '@/lib/utils'
import React from 'react'

const BicycleIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M20 9a1 1 0 1 0 0 2h3.313l2.308 6h-6.203l-.77-2H20a1 1 0 1 0 0-2h-5a1 1 0 1 0 0 2h1.577c0 .12.021.24.067.359L19.198 22h-2.281A6.002 6.002 0 0 0 5 23a6 6 0 0 0 11.917 1h6.166A6.002 6.002 0 0 0 35 23a6 6 0 0 0-6-6h-1.236l-2.584-6.718A2 2 0 0 0 23.313 9H20Zm4.528 10a5.98 5.98 0 0 0-1.445 3h-1.742l-1.154-3h4.34Zm-9.371 5.722a4.5 4.5 0 1 1 0-3.444.5.5 0 1 1-.924.383 3.5 3.5 0 1 0 0 2.679.5.5 0 0 1 .924.382Zm14.151-6.211a4.5 4.5 0 1 1-3.265 1.097.5.5 0 1 1 .657.753 3.5 3.5 0 1 0 2.54-.853.5.5 0 1 1 .068-.997Z" fill="currentColor" />
        </svg>
    )
}

export default BicycleIcon 