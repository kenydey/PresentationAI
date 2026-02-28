import { cn } from '@/lib/utils'
import React from 'react'

const PersonIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M20 4a3 3 0 0 0-3 3v1a3 3 0 1 0 6 0V7a3 3 0 0 0-3-3ZM16.893 17.748c.017-.115-.145-.16-.19-.053l-2.183 5.093A2 2 0 0 1 12.68 24h-.923a.5.5 0 0 1-.46-.697L14 17l.994-2.486A4 4 0 0 1 18.708 12h2.584a4 4 0 0 1 3.714 2.514L26 17l2.701 6.303a.5.5 0 0 1-.46.697h-.922a2 2 0 0 1-1.838-1.212l-2.183-5.093c-.046-.108-.207-.062-.191.053L24 24l.955 11.459a.5.5 0 0 1-.498.541h-.763a2 2 0 0 1-1.973-1.671L20.1 24.592c-.019-.112-.179-.112-.198 0l-1.622 9.737A2 2 0 0 1 16.306 36h-.763a.5.5 0 0 1-.498-.541L16 24l.893-6.252Z" fill="currentColor" />
        </svg>
    )
}

export default PersonIcon 