import { cn } from '@/lib/utils'
import React from 'react'

const StarIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M19.497 6.358c.158-.477.848-.477 1.006 0l3.178 9.582c.071.214.274.358.503.358H34.47c.512 0 .726.643.31.938l-8.32 5.922a.512.512 0 0 0-.192.58l3.178 9.581c.158.478-.4.875-.814.58l-8.321-5.922a.538.538 0 0 0-.622 0l-8.321 5.922c-.415.295-.972-.102-.814-.58l3.178-9.582a.512.512 0 0 0-.192-.58l-8.32-5.921c-.415-.295-.202-.938.31-.938h10.286c.229 0 .432-.144.502-.358l3.179-9.582Z" fill="currentColor" />
        </svg>
    )
}

export default StarIcon 